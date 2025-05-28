from django.db.models import Model, CharField

from core.constants import CLIENT_PEER


class WgClient(Model):
    comment = CharField(max_length=30, null=False, verbose_name="Comment")
    public_key = CharField(max_length=44, null=False, verbose_name="User's public key")
    private_key = CharField(max_length=44, null=False, verbose_name="User's private key")
    address = CharField(max_length=15, null=False, verbose_name="User's wg IP address")

    class Meta:
        verbose_name = "Wireguard client"
        verbose_name_plural = "Wireguard clients"

    def set_address(self) -> None:
        numbers_in_use = [int(x.address.split(".")[-1]) for x in WgClient.objects.all()]
        all_numbers = list(range(2, 255))
        for num in numbers_in_use:
            all_numbers.remove(num)
        if not all_numbers:
            raise Exception("Not free addresses")
        self.address = f"10.0.0.{all_numbers[0]}"

    @classmethod
    def get_client_peers(cls) -> str:
        return "\n\n".join([client.peer for client in cls.objects.all()])

    @property
    def peer(self) -> str:
        return CLIENT_PEER.format(self.comment, self.public_key, self.address)
