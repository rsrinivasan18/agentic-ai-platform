"""
ML Model Agent for running machine learning tasks.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import os
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.agents.base_agent import BaseAgent

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-3.5-turbo"


class MLModelAgent(BaseAgent):
    """
    ML Model Agent that can run machine learning tasks.
    """

    @classmethod
    def get_required_config_keys(cls) -> List[str]:
        """Get required config keys for ML Model agent."""
        return []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the ML Model agent.

        Args:
            config (Dict[str, Any], optional): Configuration for the agent
        """
        super().__init__(config or {})

        self.llm_model = self.config.get("llm_model", DEFAULT_MODEL)
        self.temperature = self.config.get("temperature", 0.0)
        self.available_models = {
            "linear_regression": LinearRegression,
            "logistic_regression": LogisticRegression,
            "random_forest_classifier": RandomForestClassifier,
            "random_forest_regressor": RandomForestRegressor,
        }

    def _get_llm(self):
        """Get LLM."""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required but not found")

        return ChatOpenAI(
            model_name=self.llm_model,
            temperature=self.temperature,
            openai_api_key=OPENAI_API_KEY,
        )

    def _prepare_data(
        self, data: pd.DataFrame, target_col: str, test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        """
        Prepare data for ML model training.

        Args:
            data (pd.DataFrame): Input data
            target_col (str): Target column name
            test_size (float): Test set size (proportion)

        Returns:
            Tuple: X_train, X_test, y_train, y_test
        """
        # Split into features and target
        X = data.drop(columns=[target_col])
        y = data[target_col]

        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        return X_train, X_test, y_train, y_test

    def _create_preprocessor(self, X: pd.DataFrame) -> ColumnTransformer:
        """
        Create a data preprocessor.

        Args:
            X (pd.DataFrame): Feature data

        Returns:
            ColumnTransformer: Data preprocessor
        """
        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
        categorical_features = X.select_dtypes(include=["object", "category"]).columns

        # Create preprocessors for different column types
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_features),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ],
            remainder="passthrough",
        )

        return preprocessor

    def _train_model(
        self, model_type: str, X_train: pd.DataFrame, y_train: pd.Series
    ) -> Dict[str, Any]:
        """
        Train an ML model.

        Args:
            model_type (str): Type of model to train
            X_train (pd.DataFrame): Training features
            y_train (pd.Series): Training targets

        Returns:
            Dict[str, Any]: Trained model and preprocessor
        """
        # Check if model type is supported
        if model_type not in self.available_models:
            raise ValueError(
                f"Model type '{model_type}' not supported. Available models: {list(self.available_models.keys())}"
            )

        # Create preprocessor
        preprocessor = self._create_preprocessor(X_train)

        # Create model
        model_class = self.available_models[model_type]
        model = model_class()

        # Create pipeline
        pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])

        # Train model
        pipeline.fit(X_train, y_train)

        return {"pipeline": pipeline, "model": model, "preprocessor": preprocessor}

    def _evaluate_model(
        self,
        pipeline: Pipeline,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        task_type: str,
    ) -> Dict[str, float]:
        """
        Evaluate an ML model.

        Args:
            pipeline (Pipeline): Trained model pipeline
            X_test (pd.DataFrame): Test features
            y_test (pd.Series): Test targets
            task_type (str): Type of task (classification or regression)

        Returns:
            Dict[str, float]: Evaluation metrics
        """
        # Make predictions
        y_pred = pipeline.predict(X_test)

        # Calculate metrics based on task type
        if task_type == "classification":
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average="weighted"),
                "recall": recall_score(y_test, y_pred, average="weighted"),
                "f1": f1_score(y_test, y_pred, average="weighted"),
            }
        else:  # regression
            metrics = {
                "mse": mean_squared_error(y_test, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
                "r2": r2_score(y_test, y_pred),
            }

        return metrics

    async def _explain_results(
        self, model_type: str, metrics: Dict[str, float], task_type: str
    ) -> str:
        """
        Explain model results using LLM.

        Args:
            model_type (str): Type of model
            metrics (Dict[str, float]): Evaluation metrics
            task_type (str): Type of task

        Returns:
            str: Explanation of results
        """
        # Format metrics
        metrics_text = "\n".join([f"{k}: {v:.4f}" for k, v in metrics.items()])

        # Get LLM
        llm = self._get_llm()

        # Create prompt
        prompt = PromptTemplate(
            input_variables=["model_type", "metrics", "task_type"],
            template="""
            You are an AI assistant specializing in machine learning. Explain the following model results in a clear, concise way.
            
            Model Type: {model_type}
            Task Type: {task_type}
            
            Metrics:
            {metrics}
            
            Please explain what these metrics mean and whether the model performance is good or could be improved:
            """,
        )

        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate explanation
        explanation = chain.run(
            model_type=model_type, metrics=metrics_text, task_type=task_type
        )

        return explanation

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an ML task.

        Args:
            input_data (Dict[str, Any]): Input data containing:
                - data (List[Dict]): Data to use
                - model_type (str): Type of model to train
                - target_column (str): Target column name
                - task_type (str): Type of task (classification or regression)

        Returns:
            Dict[str, Any]: ML results including metrics and explanation
        """
        # Extract input parameters
        data = input_data.get("data", [])
        model_type = input_data.get("model_type", "linear_regression")
        target_column = input_data.get("target_column")
        task_type = input_data.get("task_type", "regression")

        # Validate inputs
        if not data:
            raise ValueError("No data provided")
        if not target_column:
            raise ValueError("No target column specified")

        # Convert to DataFrame if necessary
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError(
                "Data must be a list of dictionaries or a pandas DataFrame"
            )

        # Prepare data
        X_train, X_test, y_train, y_test = self._prepare_data(df, target_column)

        # Train model
        model_result = self._train_model(model_type, X_train, y_train)

        # Evaluate model
        metrics = self._evaluate_model(
            model_result["pipeline"], X_test, y_test, task_type
        )

        # Explain results
        explanation = await self._explain_results(model_type, metrics, task_type)

        # Prepare result
        return {
            "model_type": model_type,
            "task_type": task_type,
            "target_column": target_column,
            "data_shape": df.shape,
            "metrics": metrics,
            "explanation": explanation,
        }
