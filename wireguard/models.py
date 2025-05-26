from django.db.models import Model, CharField

from core.constants import CLIENT_PEER


class WgClient(Model):
    comment = CharField(max_length=30, null=False, verbose_name="Comment")
    public_key = CharField(max_length=44, null=False, verbose_name="User's public key")
    private_key = CharField(max_length=44, null=False, verbose_name="User's private key")
    address = CharField(max_length=15, null=True, verbose_name="User's wg IP address")

    class Meta:
        verbose_name = "Wireguard client"
        verbose_name_plural = "Wireguard clients"

    @classmethod
    def get_client_peers(cls) -> str:
        return "\n\n".join([client.peer for client in cls.objects.all()])

    @property
    def peer(self) -> str:
        return CLIENT_PEER.format(self.comment, self.public_key, self.address)
