from tortoise import fields, models


class District(models.Model):
    """
    Model to store districts
    Cron will retrive vaccine availability for all the records
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
