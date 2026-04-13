import os
import json
import logging
import requests

from typing import Dict
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Asaas:

    DICT_URL = {
        "sandbox": "https://api-sandbox.asaas.com/v3",
        "production": "https://api.asaas.com/v3"
    }
    BASE_URL = DICT_URL.get(os.getenv("ASAAS_ENVIRONMENT"))

    @classmethod
    def get_headers(cls) -> Dict[str, str]:

        return {
            "Content-Type": "application/json",
            "User-Agent": "Budget API v1.0.0",
            "access_token": os.getenv("ASAAS_API_KEY")
        }
    
    @classmethod
    def get_base_url(cls):

        return cls.BASE_URL


class AsaasCustomers(Asaas):

    def __init__(self):
        super().__init__()

    
    def post_customer(self, data: Dict):
        
        base_url = super().get_base_url()
        
        if not base_url:
            raise ValueError("ASAAS_ENVIRONMENT not configured properly")
        
        endpoint = f"{base_url}/customers"
        
        try:
            response = requests.post(
                url=endpoint,
                json=data,
                headers=super().get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error while posting customer to Asaas: {e}")
            try:
                error_detail = response.json()
                logger.error(f"Asaas API error response: {error_detail}")
            except json.JSONDecodeError:
                logger.error(f"Could not parse error response: {response.text}")
            raise
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected error while posting customer to Asaas: {e}")
            raise
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Asaas: {e}")
            raise ValueError(f"Invalid JSON response from Asaas API: {e}")
        
    def delete_customer(self, data: Dict):
        
        base_url = super().get_base_url()
        
        if not base_url:
            raise ValueError("ASAAS_ENVIRONMENT not configured properly")
        
        endpoint = f"{base_url}/customers/{data['id']}"
        
        try:
            response = requests.delete(
                url=endpoint,
                headers=super().get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error while posting customer to Asaas: {e}")
            try:
                error_detail = response.json()
                logger.error(f"Asaas API error response: {error_detail}")
            except json.JSONDecodeError:
                logger.error(f"Could not parse error response: {response.text}")
            raise
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected error while posting customer to Asaas: {e}")
            raise

    def update_customer(self, data: Dict):
       
        base_url = super().get_base_url()

        if not base_url:
            raise ValueError("ASAAS_ENVIRONMENT not configured properly")

        endpoint = f"{base_url}/customers/{data['id']}"
        customer_data = {k: v for k, v in data.items() if k != 'id'}

        response = requests.post(
            url=endpoint,
            json=customer_data,
            headers=super().get_headers(),
            timeout=30
        )
        response.raise_for_status()
        return response.json()


class AsaasSubscriptions(Asaas):

    def __init__(self):
        super().__init__()


    def post_subscription(self, data: Dict):

        base_url = super().get_base_url()
        
        if not base_url:
            raise ValueError("ASAAS_ENVIRONMENT not configured properly")
        
        endpoint = f"{base_url}/subscriptions"

        try:
            response = requests.post(
                url=endpoint,
                json=data,
                headers=super().get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout while posting customer to Asaas: {e}")
            raise
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error while posting customer to Asaas: {e}")
            try:
                error_detail = response.json()
                logger.error(f"Asaas API error response: {error_detail}")
            except json.JSONDecodeError:
                logger.error(f"Could not parse error response: {response.text}")
            raise
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Unexpected error while posting customer to Asaas: {e}")
            raise
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Asaas: {e}")
            raise ValueError(f"Invalid JSON response from Asaas API: {e}")
        



