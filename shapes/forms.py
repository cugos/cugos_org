import zipfile
import tempfile
from django import forms
from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.gis.gdal import DataSource


#http://docs.djangoproject.com/en/dev/topics/http/file-uploads/
#http://www.neverfriday.com/sweetfriday/2008/09/-a-long-time-ago.html 

class UploadForm(forms.Form):

    file_obj  = forms.FileField(label=_('Upload a Zipped Shapefile'))
    # TODO:
    # collect attribute info to stick in potential model
    #title = forms.CharField(max_length=50,label=_('Title'))
    #epsg = forms.IntegerField()
    
    def clean_file_obj(self):
      f = self.cleaned_data['file_obj']
      valid_shp, error = self.validate(f)
      if not valid_shp:
        raise ValidationError("A problem occured: %s" % error)

    def handle(self,uploaded_file):
      downloaded_file = '%s/%s' % (settings.SHP_UPLOAD_DIR, uploaded_file)
      destination = open(downloaded_file, 'wb+')
      for chunk in uploaded_file.chunks():
          destination.write(chunk)
      destination.close()        

    def zip_check(self, ext, zip_file):
      if not True in [info.filename.endswith('shp') for info in zip_file.infolist()]:
        return False
      return True
      
    def validate(self,uploaded_file):
      tmp = tempfile.NamedTemporaryFile(suffix='.shp', mode = 'w')
      tmp_dir = tempfile.gettempdir()
      destination = open(tmp.name, 'wb+')
      for chunk in uploaded_file.chunks():
          destination.write(chunk)
      destination.close()
      if not zipfile.is_zipfile(tmp.name):
        return False, 'That file is not a valid Zip Archive'
      else:
        zfile = zipfile.ZipFile(tmp.name)
        if not self.zip_check('shp', zfile):
          return False, 'Found Zip Archive but no file with a .shp extension found inside.'
        elif not self.zip_check('prj', zfile):
          return False, 'You must supply a .prj file with the Shapefile to indicate the projection.'
        elif not self.zip_check('dbf', zfile):
          return False, 'You must supply a .dbf file with the Shapefile to supply attribute data.'
        elif not self.zip_check('shx', zfile):
          return False, 'You must supply a .shx file for the Shapefile to have a valid index.'
        else:
          for info in zfile.infolist():
            data = zfile.read(info.filename)
            shp_part = '%s%s' % (tmp_dir, info.filename)
            fout = open(shp_part, "wb")
            fout.write(data)
            fout.close()
            # http://code.djangoproject.com/wiki/GeoDjangoExtras#DataSource
          ds_name = zfile.infolist()[0].filename.split('.')[0]
          ds = DataSource('%s%s.shp' % (tmp_dir, ds_name))
          layer = ds[0]
          if layer.test_capability('RandomRead'):
            if ds._driver.__str__() == 'ESRI Shapefile':
              return True, None
            else:
              return False, "Sorry, we've experienced a problem on our server. Please try again later."
          else:
              return False, 'Cannot read the shapefile, data is corrupted inside the zip, please try to upload again' 