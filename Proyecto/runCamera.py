import cv2
from ultralytics import YOLO
import depthai as dai
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Inicializa las listas para almacenar los datos de detecciones por clase
boxes_data = []
abb_data = []
abb_base_data = []

anguloFovMed = 18.3
anguloFovMed2 = 30.11

# Carga el modelo YOLOv8
model = YOLO('runs/detect/train/weights/best.pt')

# Crear pipeline para la cámara y la profundidad
pipeline = dai.Pipeline()

# Crear nodos de cámara y profundidad
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)
color = pipeline.create(dai.node.ColorCamera)
xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutColor = pipeline.create(dai.node.XLinkOut)

# Configurar cámaras
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
color.setPreviewSize(640, 360)
color.setBoardSocket(dai.CameraBoardSocket.RGB)

# Configurar nodo de profundidad
stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
stereo.setSubpixel(True)
stereo.setLeftRightCheck(True)
stereo.setExtendedDisparity(False)
stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
stereo.setOutputSize(monoLeft.getResolutionWidth(), monoLeft.getResolutionHeight())

# Configurar XLinkOut
xoutDepth.setStreamName("depth")
xoutColor.setStreamName("color")
xoutDisparity = pipeline.create(dai.node.XLinkOut)
xoutDisparity.setStreamName("disparity")

# Enlazar nodos
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)
stereo.disparity.link(xoutDisparity.input)
stereo.depth.link(xoutDepth.input)
color.preview.link(xoutColor.input)

running = False
device = None

# Función para iniciar la captura de video y mostrar las anotaciones
def start_video():
    global running, device, depthQueue, colorQueue, disparityQueue
    if running:  # Evita que se inicie si ya está corriendo
        return

    running = True
    try:
        device = dai.Device(pipeline, usb2Mode=True)
        depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
        colorQueue = device.getOutputQueue(name="color", maxSize=4, blocking=False)
        disparityQueue = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
        update_frame()
    except RuntimeError as e:
        print(f"Error starting device: {e}")
        running = False

# Función para detener la captura de video
def stop_video():
    global running, device
    running = False
    if device:
        device.close()
        device = None
    print("Video stopped")

def update_frame():
    global running
    if not running:
        return
    
    try:
        depthFrame = depthQueue.get().getFrame()  # Obtener el frame de profundidad
        colorFrame = colorQueue.get().getCvFrame()  # Obtener el frame de color
        disparityFrame = disparityQueue.get().getFrame()  # Obtener el frame de disparidad

        # Realizar predicciones con YOLOv8 en el frame de color
        results = model.predict(colorFrame, conf=0.65)
        annotated_frame = results[0].plot()

        # Resetear las listas de detecciones por clase en cada frame
        boxes_data.clear()
        abb_data.clear()
        abb_base_data.clear()

        # Procesar detecciones
        for detection in results[0].boxes:
            class_id = int(detection.cls[0])
            class_name = model.names[class_id]
            x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)
            centroid_x = (x1 + x2) // 2
            centroid_y = (y1 + y2) // 2
            theta_y = (anguloFovMed / 180) * (centroid_y - 180)
            theta_x = (anguloFovMed2 / 320) * (centroid_x - 320)

            # Obtener el valor de profundidad en el centroide
            if 0 <= centroid_x < depthFrame.shape[1] and 0 <= centroid_y < depthFrame.shape[0]:
                z_value = depthFrame[centroid_y, centroid_x] / 1000
                if class_name == 'ABB':
                    h = z_value / 1000
                else:
                    h = 2.4
                x = h * np.tan(np.deg2rad(theta_x)) * (1 / 0.8887) - 0.0102
                y = h * np.tan(np.deg2rad(theta_y))
                # Dibujar un círculo en el centroide y mostrar la distancia en Z
                cv2.circle(annotated_frame, (centroid_x, centroid_y), 5, (0, 255, 0), -1)
                cv2.putText(annotated_frame, f"Z: {round(z_value, 2)} m", (centroid_x + 10, centroid_y + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                cv2.putText(annotated_frame, f"X: {round(x, 2)} m", (centroid_x + 10, centroid_y + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                cv2.putText(annotated_frame, f"Y: {round(y, 2)} m", (centroid_x + 10, centroid_y + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

                # Almacenar la detección en la lista adecuada
                detection_info = {"class": class_name, "x": x, "y": y, "z": z_value}
                if class_name == 'BOX':
                    boxes_data.append(detection_info)
                elif class_name == 'ABB':
                    abb_data.append(detection_info)
                elif class_name == 'ABB_BASE':
                    abb_base_data.append(detection_info)

        # Mostrar el frame anotado en la interfaz de tkinter
        annotated_image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=annotated_image)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)

        # Normalizar y colorear el frame de disparidad para mejor visualización
        disparityFrame = (disparityFrame * (255 / stereo.initialConfig.getMaxDisparity())).astype(np.uint8)
        disparityFrame = cv2.applyColorMap(disparityFrame, cv2.COLORMAP_JET)

        # Mostrar el frame de disparidad en la interfaz de tkinter
        disparity_image = Image.fromarray(disparityFrame)
        imgtk_disparity = ImageTk.PhotoImage(image=disparity_image)
        lbl_disparity.imgtk = imgtk_disparity
        lbl_disparity.configure(image=imgtk_disparity)

        if running:
            root.after(10, update_frame)
    except RuntimeError as e:
        print(f"Error during frame update: {e}")
        stop_video()

# Configurar la interfaz de tkinter
root = tk.Tk()
root.title("YOLOv8 Inference with Depth")

frame = ttk.Frame(root)
frame.pack()

# Crear un label para mostrar el video anotado
lbl_video = ttk.Label(frame)
lbl_video.grid(row=0, column=0)

# Crear un label para mostrar el frame de disparidad
lbl_disparity = ttk.Label(frame)
lbl_disparity.grid(row=0, column=1)

# Crear un botón para iniciar el video
btn_start = ttk.Button(root, text="Iniciar", command=start_video)
btn_start.pack()

# Crear un botón para detener el video
btn_stop = ttk.Button(root, text="Detener", command=stop_video)
btn_stop.pack()

# Mostrar un cuadro negro inicialmente en ambos labels
initial_image = np.zeros((360, 640, 3), np.uint8)
initial_image = Image.fromarray(initial_image)
initial_imgtk = ImageTk.PhotoImage(image=initial_image)

lbl_video.imgtk = initial_imgtk
lbl_video.configure(image=initial_imgtk)

lbl_disparity.imgtk = initial_imgtk
lbl_disparity.configure(image=initial_imgtk)

# Iniciar el bucle principal de tkinter
root.mainloop()
