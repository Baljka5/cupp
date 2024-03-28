from django.db import models
from cupp.store_trainer.models import StoreTrainer


# Create your models here.


class StrRent(models.Model):
    store_id = models.ForeignKey(StoreTrainer, on_delete=models.CASCADE, verbose_name="Store ID", null=True, blank=True)
    str_name = models.CharField('Салбарын нэр', blank=True, null=True, max_length=200)
    str_address = models.CharField('Албан ёсны хаяг', blank=True, null=True, max_length=200)
    lesser1 = models.CharField('Түрээслүүлэгч 1', blank=True, null=True, max_length=100)
    lesser2 = models.CharField('Түрээслүүлэгч 2', blank=True, null=True, max_length=100)
    lesser3 = models.CharField('Түрээслүүлэгч 3', blank=True, null=True, max_length=100)
    phone_number1 = models.IntegerField('Холбоо барих утас 1', blank=True, null=True, default=0)
    phone_number2 = models.IntegerField('Холбоо барих утас 2', blank=True, null=True, default=0)
    phone_number3 = models.IntegerField('Холбоо барих утас 2', blank=True, null=True, default=0)
    email = models.EmailField('И-майл хаяг', blank=True, null=True)
    area_size = models.IntegerField('Талбайн нийт хэмжээ м.кв', blank=True, null=True)
    cont_type = models.BooleanField('Гэрээний төрөл', blank=True, null=True)
    cntr_num1 = models.CharField('Гэрээний дугаар 1', blank=True, null=True, max_length=30)
    cntr_num2 = models.CharField('Гэрээний дугаар 2', blank=True, null=True, max_length=30)
    cntr_num3 = models.CharField('Гэрээний дугаар 3', blank=True, null=True, max_length=30)
    st_dt = models.DateField('Гэрээ эхлэх хугацаа', blank=True, null=True)
    ed_dt = models.DateField('Дуусах хугацаа ', blank=True, null=True)
    ext_ed_dt = models.DateField('Сунгагдсан хугацаа', blank=True, null=True)
    hand_over_dt = models.DateField('Талбай хүлээлцсэн актын өдөр', blank=True, null=True)
    rent_mo_fee = models.IntegerField('Түрээсийн төлбөр ', blank=True, null=True, default=0)
    rent_mo_fee_annex1 = models.IntegerField('Түрээсийн төлбөр 1', blank=True, null=True, default=0)
    rent_mo_fee_annex2 = models.IntegerField('Түрээсийн төлбөр 2', blank=True, null=True, default=0)
    rent_mo_fee_annex3 = models.IntegerField('Түрээсийн төлбөр 3', blank=True, null=True, default=0)
    deposit_amount = models.IntegerField('Барьцаа төлбөр', blank=True, null=True, default=0)
    association_no = models.CharField('СӨХ гэрээний дугаар ', blank=True, null=True, max_length=30)
    association_fee = models.IntegerField('СӨХ-ийн төлбөр', blank=True, null=True, default=0)
    manage_cnt_no = models.CharField('Менежемент гэрээний дугаар', blank=True, null=True, max_length=30)
    manage_fee = models.IntegerField('Менежментийн төлбөр', blank=True, null=True, default=0)
    exp_inc = models.CharField('Гэрээнд орсон зардал', blank=True, null=True, max_length=30)
    other_cnt = models.CharField('Бусад орлого болон зардлын гэрээ', blank=True, null=True, max_length=30)
    stora_yn = models.BooleanField('Stora box', blank=True, null=True)
    stora_fee = models.IntegerField('Stora box түрээсийн төлбөр', blank=True, null=True, default=0)
    atm_yn = models.BooleanField('ATM', blank=True, null=True)
    atm_fee = models.IntegerField('ATM түрээсийн төлбөр', blank=True, null=True, default=0)
    sublet_yn = models.BooleanField('Дамжуулан түрээслэх боломжтой эсэх', blank=True, null=True)
    sublet1_cnt_no = models.CharField('1 Дамжуулан түрээсийн гэрээний дугаар', blank=True, null=True, max_length=30)
    sublet1_size = models.IntegerField('1 Дамжуулан түрээсийн талбай хэмжээ', blank=True, null=True, default=0)
    sublet1_rent = models.IntegerField('1 Дамжуулан түрээсийн үнэ ', blank=True, null=True, default=0)
    sublet1_deposit = models.IntegerField('1 Дамжуулан түрээсийн барьцаа төлбөр', blank=True, null=True, default=0)
    sublet2_cnt_no = models.CharField('2 Дамжуулан түрээсийн гэрээний дугаар', blank=True, null=True, max_length=30)
    sublet2_size = models.IntegerField('2 Дамжуулан түрээсийн талбай хэмжээ', blank=True, null=True, default=0)
    sublet2_rent = models.IntegerField('2 Дамжуулан түрээсийн үнэ', blank=True, null=True, default=0)
    sublet2_deposit = models.IntegerField('2 Дамжуулан түрээсийн барьцаа төлбөр', blank=True, null=True, default=0)
    sublet3_cnt_no = models.CharField('3 Дамжуулан түрээсийн гэрээний дугаар', blank=True, null=True, max_length=30)
    sublet3_size = models.IntegerField('3 Дамжуулан түрээсийн талбай хэмжээ', blank=True, null=True, default=0)
    sublet3_rent = models.IntegerField('3 Дамжуулан түрээсийн үнэ', blank=True, null=True, default=0)
    sublet3_deposit = models.IntegerField('3 Дамжуулан түрээсийн барьцаа төлбөр', blank=True, null=True, default=0)
    letter = models.CharField('Албан бичиг', blank=True, null=True, max_length=30)
    notice = models.CharField('Өргөдөл', blank=True, null=True, max_length=200)
    other_cont = models.CharField('Бусад гэрээ', blank=True, null=True, max_length=200)
    franchise_yn = models.BooleanField('Франчайз санал болгох заалттай', blank=True, null=True)
    fr_rent_yn = models.BooleanField('Дамжуулан түрээсийн заалт', blank=True, null=True)
    dedication = models.BooleanField('Үл хөдлөх хөрөнгийн зориулалт', blank=True, null=True)
    notariat_yn = models.BooleanField('Нотариат', blank=True, null=True)
    real_estate_yn = models.BooleanField('ҮХХ-н гэрчилгээтэй эсэх', blank=True, null=True)
    special_terms = models.CharField('Гэрээний онцгой нөхцөл', blank=True, null=True, max_length=30)
    cont_resp_term = models.CharField('Гэрээний хариуцлагын заалт', blank=True, null=True, max_length=50)
    cont_link = models.CharField('Гэрээний холбоос', blank=True, null=True, max_length=50)

    def __str__(self):
        return self.store_id

    class Meta:
        db_table = 'str_rent'
        verbose_name = 'Rent'
