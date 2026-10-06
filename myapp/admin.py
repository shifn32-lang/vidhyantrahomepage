from django.contrib import admin

from myapp.models import ContactInquiry, NewsletterSubscriber

admin.site.site_header = 'Vidhyantra Admin'
admin.site.site_title = 'Vidhyantra Admin'
admin.site.index_title = 'Website submissions'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at', 'is_handled')
    list_editable = ('is_handled',)
    list_filter = ('is_handled', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('name', 'email', 'phone', 'service', 'message', 'created_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return False
