import logging

from urllib.parse import urlparse

from lxml.etree import LxmlError
from lxml.html import fromstring, tostring

from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from ..constants import status
from ..models import MediaFile
from .custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class CustomContentModelForm(CustomModelForm):
    """
    Form for the content model forms for pages, events and POIs.
    """

    def content_clean_method(self, field_name):
        """
        Validate the content (text/description) field (see :ref:`overriding-modelform-clean-method`) and applies changes
        to ``<img>``- and ``<a>``-Tags to match the guidelines.

        :param field_name: the name of the field which is cleaned
        :type field_name: str

        :raises ~django.core.exceptions.ValidationError: When a heading 1 (``<h1>``) is used in the text content

        :return: The valid content
        :rtype: str
        """
        try:
            content = fromstring(self.cleaned_data[field_name])
        except LxmlError:
            # The content is not guaranteed to be valid html, for example it may be empty
            return self.cleaned_data[field_name]

        # Convert heading 1 to heading 2
        for heading in content.iter("h1"):
            heading.tag = "h2"
            logger.debug("Replaced heading 1 with heading 2: %r", tostring(heading))

        # Convert pre and code tags to p tags
        for monospaced in content.iter("pre", "code"):
            tag_type = monospaced.tag
            monospaced.tag = "p"
            logger.debug(
                "Replaced %r tag with p tag: %r", tag_type, tostring(monospaced)
            )

        # Remove external links
        for link in content.iter("a"):
            link.attrib.pop("target", None)
            logger.debug("Removed target attribute from link: %r", tostring(link))

        # Scan for media files in content and replace alt texts
        for image in content.iter("img"):
            logger.debug("Image tag found in content (src: %s)", image.attrib["src"])
            # Remove host
            relative_url = urlparse(image.attrib["src"]).path
            # Remove media url prefix if exists
            if relative_url.startswith(settings.MEDIA_URL):
                relative_url = relative_url[len(settings.MEDIA_URL) :]
            # Check whether media file exists in database
            media_file = MediaFile.objects.filter(
                Q(file=relative_url) | Q(thumbnail=relative_url)
            ).first()
            # Replace alternative text
            if media_file and media_file.alt_text:
                logger.debug("Image alt text replaced: %r", media_file.alt_text)
                image.attrib["alt"] = media_file.alt_text

        return tostring(content, with_tail=False).decode("utf-8")

    def add_success_message(self, request):
        """
        This adds a success message for a translation form.
        Requires the attributes "title", "status" and "foreign_object" on the form instance.

        :param request: The current request submitting the translation form
        :type request: ~django.http.HttpRequest
        """
        model_name = type(self.instance.foreign_object)._meta.verbose_name.title()
        if not self.instance.status == status.PUBLIC:
            messages.success(
                request,
                _('{} "{}" was successfully saved as draft').format(
                    model_name, self.instance.title
                ),
            )
        elif "status" not in self.changed_data:
            messages.success(
                request,
                _('{} "{}" was successfully updated').format(
                    model_name, self.instance.title
                ),
            )
        else:
            messages.success(
                request,
                _('{} "{}" was successfully published').format(
                    model_name, self.instance.title
                ),
            )
