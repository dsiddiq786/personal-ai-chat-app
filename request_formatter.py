from typing import Dict, List, Union

class RequestFormatter:
   
    @staticmethod
    def format_instances(instances: Union[Dict, List[Dict]]) -> List[Dict]:
        
        """
        Ensures the input is formatted as a list of dictionaries.

        :param instances: A dictionary or list of dictionaries containing model input.
        :return: A properly formatted list of dictionaries.
        """
        return instances if isinstance(instances, list) else [instances]
