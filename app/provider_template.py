# Copy this pattern into app/providers/your_provider.py
# and replace PlaceholderProvider in app/main.py.
#
# from .providers.base import MediaProvider, MediaAsset
#
# class YourProvider(MediaProvider):
#     async def resolve(self, identifier, media_type):
#         # Call your authorized catalog/service here.
#         # Return a short-lived HTTPS URL to media you may distribute.
#         return MediaAsset(
#             url="https://authorized-provider.example/media/file",
#             content_type="audio/mpeg",
#             filename=f"{identifier}.mp3",
#         )
