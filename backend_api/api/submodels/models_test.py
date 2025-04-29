from django.db import models
from django.contrib.auth.models import User
# from api.models import CustomUser
# from django.contrib.auth import get_user_model


# CustomUser = get_user_model() 
    
class NFT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nfts')
    token_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    image_url = models.TextField()
    staked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Token ID: {self.token_id})"
    
class Race(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('started', 'Started'), ('ended', 'Ended')],
        default='pending'
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    winner_nft = models.ForeignKey(
        'NFT', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_races'
    )

    def __str__(self):
        return f"Race: {self.name} (Status: {self.status})"
    

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    nft = models.ForeignKey('NFT', on_delete=models.CASCADE, related_name='bets')
    race = models.ForeignKey('Race', on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bet by {self.user.username} on Race: {self.race.name} with NFT: {self.nft.name} (Amount: {self.amount})"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    nft = models.ForeignKey('NFT', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    tx_type = models.CharField(
        max_length=50,
        choices=[
            ('mint', 'Mint'),
            ('stake', 'Stake'),
            ('unstake', 'Unstake'),
            ('win', 'Win')
        ]
    )
    tx_hash = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.tx_type} by {self.user.username} (TxHash: {self.tx_hash})"