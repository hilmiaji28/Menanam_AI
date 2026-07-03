import time
import requests

from config import FASTAPI_URL


class APIClient:

    def __init__(self):

        self.base_url = FASTAPI_URL
        self.timeout = 120
        self.max_retry = 3

    # =====================================================
    # INTERNAL REQUEST
    # =====================================================

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ):

        url = f"{self.base_url}{endpoint}"

        last_error = None

        for attempt in range(self.max_retry):

            try:

                response = requests.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs,
                )

                response.raise_for_status()

                return response.json()

            except requests.exceptions.ConnectionError:

                last_error = (
                    "Tidak dapat terhubung ke backend."
                )

            except requests.exceptions.Timeout:

                last_error = (
                    "Permintaan melebihi batas waktu."
                )

            except requests.exceptions.HTTPError:

                try:

                    return response.json()

                except Exception:

                    last_error = (
                        f"HTTP Error {response.status_code}"
                    )

            except Exception as e:

                last_error = str(e)

            # retry
            if attempt < self.max_retry - 1:

                time.sleep(1)

        return {
            "error": last_error
        }

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self):

        return self._request(
            "GET",
            "/health",
        )

    # =====================================================
    # PREDICTION
    # =====================================================

    def predict(
        self,
        payload: dict,
    ):

        return self._request(
            "POST",
            "/predict",
            json=payload,
        )

    # =====================================================
    # AI ASSISTANT
    # =====================================================

    def assistant(
        self,
        question: str,
        history=None,
    ):

        payload = {
            "question": question,
            "history": history or [],
        }

        return self._request(
            "POST",
            "/assistant",
            json=payload,
        )


api = APIClient()