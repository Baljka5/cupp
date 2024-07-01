from django.utils import timezone

from django.db import models as m


# Create your models here.

class StoreCompetitors(m.Model):
    store_id = m.CharField('Дэлгүүрийн дугаар', blank=True, null=True, max_length=5)
    store_name = m.CharField('Салбарын нэр', null=True, max_length=200)
    comp_yn = m.BooleanField('Урсгалд нөлөөлөх өрсөлдөгч байгаа эсэх', blank=True, null=True)
    comp_type = m.ForeignKey('DimCompType', on_delete=m.CASCADE, blank=False, null=False)
    comp_name = m.CharField('Өрсөлдөгчийн нэр', blank=True, null=True, max_length=50)
    comp_range_meter = m.FloatField('Өрсөлдөгчийн манай дэлгүүрээс ойролцоогоор хэдэн метерт', blank=True, null=True,
                                    default=0)
    comp_cluster = m.ForeignKey('DimCluster', on_delete=m.CASCADE, blank=False, null=False)
    comp_open_dt = m.DateField('Өрсөлдөгч хэзээ нээсэн', blank=True, null=True, default='')
    comp_status = m.BooleanField('Өрсөлдөгч хэвийн ажиллаж байгаа', blank=True, null=True)
    comp_close_dt = m.DateField('Өрсөлдөгч хаасан бол хэзээ хаасан', blank=True, null=True, default='')
    comp_schedule_tp = m.CharField('Өрсөлдөгчийн цагийн хуваарийн төрөл', blank=True, null=True, max_length=10)
    comp_schedule_time = m.CharField("Өрсөлдөгчийн цагийн хуваарь", null=True, blank=True, max_length=11)
    comp_size = m.FloatField("Өрсөлдөгчийн талбай", blank=True, null=True, default=0)
    comp_shelf_qty = m.IntegerField("Өрсөлдөгчийн лангууны тоо", default=0, blank=True, null=True)
    comp_alcohol = m.BooleanField("Өрсөлдөгч архи зардаг эсэх", blank=True, null=True)
    comp_tabacco = m.BooleanField("Өрсөлдөгч тамхи зардаг эсэх", blank=True, null=True)
    comp_delivery = m.BooleanField("Өрсөлдөгч хүргэлттэй эсэх", blank=True, null=True)
    comp_pros = m.CharField("Өрсөлдөгчийн давуу тал", blank=True, null=True, max_length=50, default='')
    comp_long = m.CharField("Өрсөлдөгчийн Уртраг", blank=True, null=True, max_length=50, default=0)
    comp_latt = m.CharField("Өрсөлдөгчийн Өргөрөг", blank=True, null=True, max_length=50, default=0)

    def __str__(self):
        return self.comp_type.comp_tp

    class Meta:
        db_table = "store_competitors"
        verbose_name = "Store Competitors"


class DimCluster(m.Model):
    common_code = m.CharField("Common Code", max_length=10, primary_key=True)
    common_code_name = m.CharField("Common Code Name", blank=True, null=True, max_length=50)

    def __str__(self):
        return self.common_code_name

    class Meta:
        db_table = 'dim_cluster'
        verbose_name = 'Dim Cluster'


class DimCompType(m.Model):
    comp_tp = m.CharField("Competitor Type", max_length=50, primary_key=True)
    description = m.CharField("Description", blank=True, null=True, max_length=255)

    def __str__(self):
        return self.comp_tp

    class Meta:
        db_table = "dim_comp_type"
        verbose_name = "Competitor Type"
