from ultralytics import YOLO

class object_detection:

    def __init__(self):
        # Load a pretrained YOLOv8n model
        self._model = YOLO("yolov8n.pt")
        self._objects = []

    def detect(self, image):
        '''
            returns a list of recognized objects defined in dict of their   
            boundry box dimension and their name - 
            bounding_box = (x, y, w, h) (x, y of top left corner)
        '''
        # Run inference on the source
        _results = self._model(image, save=False)  # list of Results _objects
        for obj in _results:
            _boxes = obj.boxes
            for box in _boxes:
                _box_dimensions_tensor = box.xywh
                _box_dimensions_tensor = _box_dimensions_tensor[0].int()

                ### convert tensor int to regular int
                _x, _y, _w, _h = _box_dimensions_tensor[0].item(), _box_dimensions_tensor[1].item(), _box_dimensions_tensor[2].item(), _box_dimensions_tensor[3].item()
                _box_dimension = (_x-int(_w/2),_y-int(_h/2),_w,_h)

                ### name of the objects
                _cls_id = box.cls  # Class ID of the detected object
                _obj_name = self._model.names[int(_cls_id)]  # Convert class ID to class name

                _object = {'bounding_box':_box_dimension, 'name':_obj_name}
                self._objects.append(_object)
        return self._objects

    def _in_object(self, point, box):
        '''
            this point is inside the box or not
            point : x, y
            box: x, y, w, h (x, y of top left corner)
        '''
        point_x, point_y = point
        box_x, box_y, box_w, box_h = box
        print(f"########################### point :{point}, BOX : {box} ################################")
        toleranse = 20 
        if ((point_x > abs(box_x-toleranse) and point_x < box_x+box_w+toleranse) and
            (point_y > abs(box_y-toleranse) and point_y < box_y+box_h+toleranse)):
            print("******************************************** YOU GOT IT **************************")
            return True
        else:
            return False
        
    def is_on_object(self, point):
        '''
            Point is on an object or not
            point is a list of x, y  
            ex: point = [510, 320]
        '''
        _obj_detected = False
        _obj_data = {}
        for obj in self._objects:
            _obj_boundry_box = obj['bounding_box']
            if self._in_object(point,_obj_boundry_box): ### point inside the object
                _obj_detected = True
                _obj_data = obj
                break
        if _obj_detected == True:
            return _obj_data
        else:
            return False



if __name__ == "__main__":
    objects = object_detection()

    # Define path to the image file
    source = "./detected_image.jpg"
    check_point = [592, 397]
    check_point2 = [10, 20]
    object_data = objects.detect(source)
    print(object_data)
    print(objects.is_on_object(check_point2))
