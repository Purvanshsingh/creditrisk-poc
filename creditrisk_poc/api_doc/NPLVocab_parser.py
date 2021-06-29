import json
import os
from hydra_python_core.doc_writer import HydraClass, HydraClassProp, HydraClassOp, HydraStatus


def get_npl_vocab() -> dict:
    vocab_file_path = os.path.join(os.path.dirname(os.getcwd()), "npl_vocab/NonPerformingLoan.jsonld")
    npl_vocab_file = open(vocab_file_path)
    npl_vocab = json.load(npl_vocab_file)
    return npl_vocab


def get_all_classes(vocab: dict) -> list:
    """
    Get all the classes from the given Vocabulary.
    """
    classes = list()
    defines = vocab['defines']
    for obj in defines:
        if obj['@type'] == 'rdfs:Class':
            classes.append(obj)
    return classes


def create_hydra_classes(vocab_classes: list) -> list:
    """
    Create hydra classes from list of vocab classes.
    """
    hydra_classes = list()
    for class_ in vocab_classes:
        hydra_class = HydraClass(class_['rdfs:label'], class_['rdfs:comment'], endpoint=True)
        hydra_classes.append(hydra_class)
    return hydra_classes


def get_class_properties(class_ : str, vocab : dict) -> list:
    """
    Return all the properties of the given class.
    """
    properties = list()
    defines = vocab['defines']
    for obj in defines:
        if obj.get('propertyOf'):
            propertyof = obj['propertyOf']['@id'].split('#')[1]
            if propertyof == class_ or obj['@type'] == 'owl:DataProperty' and obj['@type'] == 'owl:ObjectProperty':
                properties.append(obj)
    return properties


def create_hydra_properties(property_: dict, hydra_classes: dict) -> HydraClassProp:
    if property_.get('propertyOn') and isinstance(property_['propertyOn'], dict):
        property_on_class = property_.get("propertyOn")['@id'].split('#')[1]
        property_uri = hydra_classes[property_on_class].id_
    else:
        property_uri = property_['@id']
    hydra_property = HydraClassProp(property_uri, property_['rdfs:label'],
                                    required=True, read=True, write=True)
    return hydra_property


def get_class_id(class_name: str, hydra_classes: list):
    """
    Returns the class id of given class.
    """
    for class_ in hydra_classes:
        if class_.title == class_name:
            return class_.id_


def add_operations_to_class(hydra_classes: list, class_name: str, operations: list) -> list:
    """
    Return list of hydra properties of given class.
    """
    hydra_operations = []
    class_id = get_class_id(class_name, hydra_classes)
    if class_id:
        for operation in operations:
            if operation == "GET":
                get_operation_status = [HydraStatus(code=200, desc=class_name + " class returned.")]
                op = HydraClassOp(class_name + operation, operation, None, class_id, [], [], get_operation_status)
                hydra_operations.append(op)
            if operation == "PUT":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class Added.")]
                op = HydraClassOp(class_name + operation, operation, class_id, None, [], [], put_operation_status)
                hydra_operations.append(op)
            if operation == "POST":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class updated.")]
                op = HydraClassOp(class_name + operation, operation, class_id, None, [], ["Content-Type", "Content-Length"],
                                  put_operation_status)
                hydra_operations.append(op)
            if operation == "DELETE":
                put_operation_status = [HydraStatus(code=200, desc=class_name + " class Deleted.")]
                op = HydraClassOp(class_name + operation, operation, None, None, [], [],
                                  put_operation_status)
                hydra_operations.append(op)
    return hydra_operations






