from django import forms


class BootstrapFormMixin:
    """اضافه کردن خودکار کلاس‌های Bootstrap 5 به همه فیلدهای فرم"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs["class"] = (widget.attrs.get("class", "") + " form-check-input").strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = (widget.attrs.get("class", "") + " form-select").strip()
            else:
                widget.attrs["class"] = (widget.attrs.get("class", "") + " form-control").strip()
            if field.help_text:
                widget.attrs.setdefault("aria-describedby", f"{field_name}_help")
