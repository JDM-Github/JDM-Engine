from typing import List
from engine.controllers.base_controller import BaseController
from engine.ui.window import EngineWindow

def load_controllers(window: EngineWindow, controller_classes: List[BaseController]):
    instances: list[BaseController] = []

    for controller_cls in controller_classes:
        controller: BaseController = controller_cls(window)
        controller.connect()
        instances.append(controller)
    
    return instances
