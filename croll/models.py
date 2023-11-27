from django.db import models

class TbCroll(models.Model):
    posttitle = models.TextField(db_column='post_title', null=False)
    search_txt = models.TextField(db_column='search_txt', null=True)
    blogurl = models.TextField(db_column='blog_url', null=True)
    createdat = models.DateField(db_column='created_at', null=True)

    class Meta:
        managed = False
        db_table = 'TB_CROLL'

    def __str__(self):
        return "제목 : " + self.posttitle
