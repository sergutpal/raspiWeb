# -*- coding: utf-8 -*-
"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from raspiWeb.views import inicio, inicioFull, auto, alarma, musica, musica1OR4, \
                    kodi, foto, reboot, watchdog, temperatura, parking, \
                    wakeonlan, transmissionON, transmissionOFF, firewallON, \
                    firewallOFF

urlpatterns = [
    url(r'^accounts/login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'admin/login.html'}),
    url(r'^admin/', admin.site.urls),
    url(r'^$', inicio),
    url(r'^inicio/$', inicioFull),
    url(r'^auto/(on|off)/$', auto),
    url(r'^alarma/(on|off)/$', alarma),
    url(r'^musica/(on|off)/$', musica),
    url(r'^m/(1|4)/$', musica1OR4),
    url(r'^kodi/(1|2|3)/$', kodi),
    url(r'^foto/$', foto),
    url(r'^foto/(\d)/$', foto),
    url(r'^reboot/$', reboot),
    url(r'^reboot/(\d)/$', reboot),
    url(r'^watchdog/$', watchdog),
    url(r'^watchdog/(\d)/$', watchdog),
    url(r'^temperatura/$', temperatura),
    url(r'^temperatura/(\d)/$', temperatura),
    url(r'^parking/$', parking),
    url(r'^parking/(\d{1,4})/$', parking),
    url(r'^wakeonlan/$', wakeonlan),
    url(r'^transmissionON/$', transmissionON),
    url(r'^transmissionOFF/$', transmissionOFF),
    url(r'^firewallON/$', firewallON),
    url(r'^firewallOFF/$', firewallOFF),
]
