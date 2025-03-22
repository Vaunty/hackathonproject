import cv2

import numpy as np

def load_yolo():

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    with open("coco.names", "r") as f:

        classes = [line.strip() for line in f.readlines()]

    return net, classes, output_layers



def detect_objects(img, net, output_layers):

    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outputs = net.forward(output_layers)

    return outputs, width, height



def draw_labels(outputs, img, classes, width, height):

    boxes = []

    confidences = []

    class_ids = []

    for output in outputs:

        for detection in output:

            scores = detection[5:]

            class_id = np.argmax(scores)

            confidence = scores[class_id]

            if confidence > 0.5:

                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype("int")

                x = int(center_x - w / 2)

                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])

                confidences.append(float(confidence))

                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in indices.flatten():

        x, y, w, h = boxes[i]

        label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img



def main():

    net, classes, output_layers = load_yolo()

    cap = cv2.VideoCapture(0)  # Open webcam (use video file path instead if needed)

    while True:

        ret, frame = cap.read()

        if not ret:

            break

        outputs, width, height = detect_objects(frame, net, output_layers)

        frame = draw_labels(outputs, frame, classes, width, height)

        cv2.imshow("Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

    cap.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()