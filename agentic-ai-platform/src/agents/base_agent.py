"""
Base agent class for the Agentic AI Platform.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the platform.

    This provides a common interface that all agents will implement,
    making it easier to swap or compose agents in the future.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent with optional configuration.

        Args:
            config (Dict[str, Any], optional): Configuration for the agent
        """
        self.config = config or {}
        self.name = self.config.get("name", self.__class__.__name__)
        self.description = self.config.get("description", "")

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Process input data and return results.

        Args:
            input_data (Any): The input data to process

        Returns:
            Any: The processing results
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about this agent.

        Returns:
            Dict[str, Any]: Agent metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "config": self.config,
        }

    @classmethod
    def get_required_config_keys(cls) -> List[str]:
        """
        Get the required configuration keys for this agent.

        Returns:
            List[str]: List of required configuration keys
        """
        return []

    def validate_config(self) -> bool:
        """
        Validate that the agent has all required configuration.

        Returns:
            bool: True if the configuration is valid, False otherwise
        """
        required_keys = self.get_required_config_keys()
        return all(key in self.config for key in required_keys)
