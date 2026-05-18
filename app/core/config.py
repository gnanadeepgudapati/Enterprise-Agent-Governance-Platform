from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

	app_name: str = "Enterprise Agent Governance Platform"
	app_version: str = "1.0.0"
	environment: str = "dev"

	request_timeout_seconds: float = 2.0
	agent_timeout_seconds: float = 0.25
	min_score_threshold: float = 65.0
	sensitive_topic_score_threshold: float = 80.0
	max_alerts_kept: int = 200

	# Controlled delay helps mimic realistic heterogeneous services in tests.
	enable_synthetic_delay: bool = True


settings = Settings()
