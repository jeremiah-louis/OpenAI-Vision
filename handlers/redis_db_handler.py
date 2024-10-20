import uuid
import redis


class RedisHandler:
    def __init__(self) -> None:
        self.r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    def generate_unique_uuid(self, user_id: str) -> str:
        unique_id: str = f"{user_id}_{uuid.uuid4()}"
        return unique_id

    def store_list_in_redis(self, urls: list[str], document_id: str) -> None:
        """
        Stores a list of Cloudinary PDF-image URLs in the Redis database, with a unique key.

        Args:
            urls: List of image URLs corresponding to PDF pages
            user_id: Identifier coming from user's credentials to create a unique key
        """
        url_to_string: str = " ".join(urls)
        self.r.set(name=document_id, value=url_to_string)

    def retrieve_list_from_redis(self, document_id: str) -> list[str]:
        """
        Retrieves the list of Cloudinary PDF-image from the Redis database.

        Args:
            document_id: Identifier coming from user's credentials to create a unique key.

        Returns:
            list: list of Cloudinary PDF-image URLs.
        """
        url_list = self.r.get(document_id)
        return str(url_list).split()
