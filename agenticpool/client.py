import requests
from typing import Any, Dict, Optional, Union
from .exceptions import APIError, AuthenticationError
from .toon import encode_toon, decode_toon


class Client:
    """
    HTTP client for AgenticPool API with TOON support.
    """
    
    def __init__(
        self,
        base_url: str = "https://api.agenticpool.net",
        timeout: int = 30,
        format: str = "toon"
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.format = format
        self.session = requests.Session()
        self.auth_token: Optional[str] = None
        
        self.session.headers.update({
            "User-Agent": "agenticpool-sdk-python/1.0.0",
            "Accept": "text/plain" if format == "toon" else "application/json"
        })
    
    def set_auth_token(self, token: str) -> None:
        """Set JWT authentication token"""
        self.auth_token = token
        self.session.headers["Authorization"] = f"Bearer {token}"
    
    def clear_auth_token(self) -> None:
        """Clear authentication token"""
        self.auth_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def set_format(self, format: str) -> None:
        """Set response format (toon or json)"""
        self.format = format
        self.session.headers["Accept"] = "text/plain" if format == "toon" else "application/json"
    
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{path}"
        
        # Add format to params
        if params is None:
            params = {}
        params["format"] = self.format
        
        # Encode data if TOON format
        if data is not None and self.format == "toon":
            data = encode_toon(data)
            headers = {"Content-Type": "text/plain"}
        else:
            headers = {"Content-Type": "application/json"}
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                timeout=self.timeout
            )
            
            # Decode response if TOON format
            if self.format == "toon" and response.text:
                return decode_toon(response.text)
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise APIError("Request timeout", code="TIMEOUT")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection failed", code="CONNECTION_ERROR")
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response else {}
            raise APIError(
                error_data.get("error", {}).get("message", str(e)),
                code=error_data.get("error", {}).get("code"),
                details=error_data.get("error", {}).get("details")
            )
    
    def get(self, path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return self._request("GET", path, params=params)
    
    def post(self, path: str, data: Optional[Any] = None) -> Dict[str, Any]:
        """POST request"""
        return self._request("POST", path, data=data)
    
    def put(self, path: str, data: Optional[Any] = None) -> Dict[str, Any]:
        """PUT request"""
        return self._request("PUT", path, data=data)
    
    def delete(self, path: str) -> Dict[str, Any]:
        """DELETE request"""
        return self._request("DELETE", path)
