import os
import sys
import json
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coderr.settings")
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from market_app.models import Profiles, Reviews, Offers, OffersDetails


#___________________________________________ User ___________________________________________

user1 = User.objects.create_user(username = "Lea", password="test", email="lea@web.de")
user2 = User.objects.create_user(username = "Felix", password="test", email="felix@web.de")
user3 = User.objects.create_user(username = "Marcel", password="test", email="marcel@web.de")
user4 = User.objects.create_user(username = "Sebastian", password="test", email="sebastian@web.de")
user5 = User.objects.create_user(username = "andrey", password="asdasd", email="andrey@web.de")
user6 = User.objects.create_user(username = "kevin", password="asdasd24", email="kevin@web.de")

profil1 = Profiles.objects.create(user=user1, type="customer", tel="0176-899793", location="Bad Berginssee")
profil2 = Profiles.objects.create(user=user2, type="business", tel="0176-100257", location="Flachbach")
profil3 = Profiles.objects.create(user=user3, type="customer", tel="0176-872506", location="Kielsloh")
profil4 = Profiles.objects.create(user=user4, type="business", tel="0176-983124", location="Bahnstop")
profil5 = Profiles.objects.create(user=user5, type="customer", tel="0176-641421", location="Bad Kaktus")
profil6 = Profiles.objects.create(user=user6, type="business", tel="0176-154120", location="Quellental")


#___________________________________________ Reviews ___________________________________________

review1 = Reviews.objects.create(rating = 3.5, reviewer=profil1, business_user=profil2, description="Die Abgabe war etwas verspätet - aber ansonsten tolle Leistung. Vielen Dank!")
review2 = Reviews.objects.create(rating = 5, reviewer=profil3, business_user=profil2, description="Keine Probleme. Ergebnis war großartig.")
review3 = Reviews.objects.create(rating = 2.5, reviewer=profil5, business_user=profil2, description="Angesichts des Preises, hätte ich da doch mehr erwartet.")

review4 = Reviews.objects.create(rating = 4.5, reviewer=profil1, business_user=profil4, description="Die Zusammenarbeithat mir sehr gefallen, gerne wieder!")
review5 = Reviews.objects.create(rating = 0.5, reviewer=profil5, business_user=profil4, description="Leistung stimmte überhaupt nicht! Ich möchte mein Geld zurück")
review6 = Reviews.objects.create(rating = 3, reviewer=profil3, business_user=profil4, description="Preis/Leistung war hier gegeben.")

review7 = Reviews.objects.create(rating = 5, reviewer=profil5, business_user=profil6, description="Eine weitere Zusammenarbeit kann ich mir sehr gut vorstellen!")
review8 = Reviews.objects.create(rating = 1.5, reviewer=profil3, business_user=profil6, description="Leistung stimmte überhaupt nicht! Ich möchte mein Geld zurück")
review9 = Reviews.objects.create(rating = 4, reviewer=profil1, business_user=profil6, description="Cooles Ergenis zum passenden Preis. Weiter so!")

#___________________________________________ Offers ___________________________________________


# profil2 - Webdesign Fokus
Offer1 = Offers.objects.create(user=profil2, title="Website-Design Paket", description="Individuelles Webdesign für kleine Unternehmen", min_price=250, min_delivery_time=7)
Offer2 = Offers.objects.create(user=profil2, title="Landingpage Erstellung", description="Professionelle Landingpage zur Lead-Generierung", min_price=150, min_delivery_time=5)
Offer3 = Offers.objects.create(user=profil2, title="Responsive Redesign", description="Modernes Redesign für mobile und Desktop-Kompatibilität", min_price=300, min_delivery_time=10)
Offer4 = Offers.objects.create(user=profil2, title="E-Commerce Design", description="Design für deinen eigenen Onlineshop", min_price=400, min_delivery_time=14)
Offer5 = Offers.objects.create(user=profil2, title="UI/UX Analyse", description="Expertenanalyse für bessere Nutzerführung", min_price=200, min_delivery_time=4)

# profil4 - Webentwicklung Fokus
Offer6 = Offers.objects.create(user=profil4, title="Fullstack Web-Entwicklung", description="Komplette Weblösung von Frontend bis Backend", min_price=800, min_delivery_time=21)
Offer7 = Offers.objects.create(user=profil4, title="API-Integration", description="Integration externer APIs in deine Website", min_price=300, min_delivery_time=5)
Offer8 = Offers.objects.create(user=profil4, title="Performance Optimierung", description="Verbesserung der Ladezeiten deiner Website", min_price=250, min_delivery_time=3)
Offer9 = Offers.objects.create(user=profil4, title="CMS-Setup", description="Installation und Einrichtung eines Content Management Systems", min_price=350, min_delivery_time=7)

# profil6 - Erweiterte Services
Offer10 = Offers.objects.create(user=profil6, title="SEO Optimierung", description="On-Page SEO für bessere Sichtbarkeit", min_price=200, min_delivery_time=4)
Offer11 = Offers.objects.create(user=profil6, title="Wartung & Support", description="Monatlicher Support für deine Webprojekte", min_price=150, min_delivery_time=30)
Offer12 = Offers.objects.create(user=profil6, title="Hosting Setup", description="Komplettes Hosting Setup inkl. Sicherheit", min_price=180, min_delivery_time=2)
Offer13 = Offers.objects.create(user=profil6, title="Web Security Check", description="Sicherheitsprüfung deiner Website", min_price=220, min_delivery_time=3)
Offer14 = Offers.objects.create(user=profil6, title="Website Migration", description="Umzug deiner Website auf einen neuen Server", min_price=300, min_delivery_time=4)


#___________________________________________ OffersDetails ___________________________________________

#  "offer_type": basic, standard, premium

# OfferDetails für Offer1
OffersDetails1 = OffersDetails.objects.create(offer=Offer1, title="Basic Design", revisions=2, delivery_time_in_days=5, price=100, offer_type="basic", features=["Logo Design", "Visitenkarte"])
OffersDetails2 = OffersDetails.objects.create(offer=Offer1, title="Standard Design", revisions=5, delivery_time_in_days=7, price=200, offer_type="standard", features=["Logo Design", "Visitenkarte", "Briefpapier"])
OffersDetails3 = OffersDetails.objects.create(offer=Offer1, title="Premium Design", revisions=10, delivery_time_in_days=10, price=500, offer_type="premium", features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"])

# OfferDetails für Offer2
OffersDetails4 = OffersDetails.objects.create(offer=Offer2, title="Web Starter", revisions=1, delivery_time_in_days=7, price=150, offer_type="basic", features=["Landingpage", "Kontaktformular"])
OffersDetails5 = OffersDetails.objects.create(offer=Offer2, title="Web Advanced", revisions=3, delivery_time_in_days=10, price=300, offer_type="standard", features=["Landingpage", "Kontaktformular", "SEO Basic"])
OffersDetails6 = OffersDetails.objects.create(offer=Offer2, title="Web Premium", revisions=7, delivery_time_in_days=14, price=700, offer_type="premium", features=["Landingpage", "Kontaktformular", "SEO Advanced", "CMS Integration"])

# OfferDetails für Offer3
OffersDetails7 = OffersDetails.objects.create(offer=Offer3, title="Shop Basic", revisions=2, delivery_time_in_days=14, price=200, offer_type="basic", features=["Produktseite", "Zahlungsintegration"])
OffersDetails8 = OffersDetails.objects.create(offer=Offer3, title="Shop Standard", revisions=4, delivery_time_in_days=18, price=400, offer_type="standard", features=["Produktseite", "Zahlungsintegration", "Versandoptionen"])
OffersDetails9 = OffersDetails.objects.create(offer=Offer3, title="Shop Premium", revisions=8, delivery_time_in_days=25, price=900, offer_type="premium", features=["Produktseite", "Zahlungsintegration", "Versandoptionen", "Erweiterte Analyse"])

# OfferDetails für Offer4
OffersDetails10 = OffersDetails.objects.create(offer=Offer4, title="SEO Basic", revisions=2, delivery_time_in_days=5, price=120, offer_type="basic", features=["Keyword-Recherche", "Onpage-Optimierung"])
OffersDetails11 = OffersDetails.objects.create(offer=Offer4, title="SEO Standard", revisions=4, delivery_time_in_days=10, price=250, offer_type="standard", features=["Keyword-Recherche", "Onpage-Optimierung", "Backlink-Analyse"])
OffersDetails12 = OffersDetails.objects.create(offer=Offer4, title="SEO Premium", revisions=6, delivery_time_in_days=15, price=600, offer_type="premium", features=["Keyword-Recherche", "Onpage-Optimierung", "Backlink-Analyse", "Content-Erstellung"])

# OfferDetails für Offer5
OffersDetails13 = OffersDetails.objects.create(offer=Offer5, title="Branding Basic", revisions=1, delivery_time_in_days=3, price=80, offer_type="basic", features=["Logo Design", "Farbschema"])
OffersDetails14 = OffersDetails.objects.create(offer=Offer5, title="Branding Standard", revisions=3, delivery_time_in_days=7, price=220, offer_type="standard", features=["Logo Design", "Farbschema", "Schriftwahl"])
OffersDetails15 = OffersDetails.objects.create(offer=Offer5, title="Branding Premium", revisions=5, delivery_time_in_days=12, price=500, offer_type="premium", features=["Logo Design", "Farbschema", "Schriftwahl", "Design Guidelines"])

# OfferDetails für Offer 6
OffersDetails16 = OffersDetails.objects.create(offer=Offer6, title="Basic Video Editing", revisions=2, delivery_time_in_days=3, price=150, offer_type="basic", features=["Videozuschnitt", "Farbanpassung"])
OffersDetails17 = OffersDetails.objects.create(offer=Offer6, title="Standard Video Editing", revisions=5, delivery_time_in_days=5, price=400, offer_type="standard", features=["Videozuschnitt", "Farbanpassung", "Übergänge"])
OffersDetails18 = OffersDetails.objects.create(offer=Offer6, title="Premium Video Editing", revisions=10, delivery_time_in_days=7, price=800, offer_type="premium", features=["Videozuschnitt", "Farbanpassung", "Übergänge", "Sounddesign"])

# Offer7 - API-Integration
OffersDetails19 = OffersDetails.objects.create(offer=Offer7, title="Basic API Integration", revisions=1, delivery_time_in_days=5, price=300, offer_type="basic", features=["Integration einer API"])
OffersDetails20 = OffersDetails.objects.create(offer=Offer7, title="Standard API Integration", revisions=3, delivery_time_in_days=7, price=500, offer_type="standard", features=["Integration mehrerer APIs", "Fehlerbehandlung"])
OffersDetails21 = OffersDetails.objects.create(offer=Offer7, title="Premium API Integration", revisions=5, delivery_time_in_days=10, price=800, offer_type="premium", features=["Mehrere APIs", "Dokumentation", "Testabdeckung"])

# Offer8 - Performance Optimierung
OffersDetails22 = OffersDetails.objects.create(offer=Offer8, title="Basic Optimierung", revisions=1, delivery_time_in_days=3, price=250, offer_type="basic", features=["Bilder komprimieren", "Cache einrichten"])
OffersDetails23 = OffersDetails.objects.create(offer=Offer8, title="Standard Optimierung", revisions=3, delivery_time_in_days=5, price=450, offer_type="standard", features=["Bilder komprimieren", "Caching", "Code-Minimierung"])
OffersDetails24 = OffersDetails.objects.create(offer=Offer8, title="Premium Optimierung", revisions=5, delivery_time_in_days=7, price=700, offer_type="premium", features=["Ladezeiten-Analyse", "Serveroptimierung", "Performance-Bericht"])

# Offer9 - CMS-Setup
OffersDetails25 = OffersDetails.objects.create(offer=Offer9, title="Basic CMS Setup", revisions=1, delivery_time_in_days=7, price=350, offer_type="basic", features=["CMS Installation", "Basis Konfiguration"])
OffersDetails26 = OffersDetails.objects.create(offer=Offer9, title="Standard CMS Setup", revisions=3, delivery_time_in_days=10, price=600, offer_type="standard", features=["CMS Installation", "Theme Einrichtung", "Basis Plugins"])
OffersDetails27 = OffersDetails.objects.create(offer=Offer9, title="Premium CMS Setup", revisions=5, delivery_time_in_days=14, price=1000, offer_type="premium", features=["CMS Installation", "Custom Theme", "Erweiterte Plugins", "Sicherheitsoptimierung"])

# Offer10 - SEO Optimierung
OffersDetails28 = OffersDetails.objects.create(offer=Offer10, title="Basic SEO", revisions=1, delivery_time_in_days=4, price=200, offer_type="basic", features=["Meta-Tags", "Basis Keywords"])
OffersDetails29 = OffersDetails.objects.create(offer=Offer10, title="Standard SEO", revisions=3, delivery_time_in_days=6, price=400, offer_type="standard", features=["Meta-Tags", "Keywords", "Seitenstruktur Optimierung"])
OffersDetails30 = OffersDetails.objects.create(offer=Offer10, title="Premium SEO", revisions=5, delivery_time_in_days=8, price=700, offer_type="premium", features=["On-Page SEO", "Keyword Recherche", "SEO-Bericht"])

# Offer11 - Wartung & Support
OffersDetails31 = OffersDetails.objects.create(offer=Offer11, title="Basic Support", revisions=0, delivery_time_in_days=30, price=150, offer_type="basic", features=["Technischer Support", "Fehlerbehebung"])
OffersDetails32 = OffersDetails.objects.create(offer=Offer11, title="Standard Support", revisions=0, delivery_time_in_days=30, price=300, offer_type="standard", features=["Technischer Support", "Fehlerbehebung", "Updates"])
OffersDetails33 = OffersDetails.objects.create(offer=Offer11, title="Premium Support", revisions=0, delivery_time_in_days=30, price=500, offer_type="premium", features=["Technischer Support", "Updates", "Sicherheitsüberwachung", "Performance Monitoring"])

# Offer12 - Hosting Setup
OffersDetails34 = OffersDetails.objects.create(offer=Offer12, title="Basic Hosting", revisions=1, delivery_time_in_days=2, price=180, offer_type="basic", features=["Hosting Einrichtung", "Basis Sicherheit"])
OffersDetails35 = OffersDetails.objects.create(offer=Offer12, title="Standard Hosting", revisions=2, delivery_time_in_days=3, price=350, offer_type="standard", features=["Hosting Einrichtung", "SSL-Zertifikat", "Backups"])
OffersDetails36 = OffersDetails.objects.create(offer=Offer12, title="Premium Hosting", revisions=3, delivery_time_in_days=4, price=600, offer_type="premium", features=["Hosting Einrichtung", "SSL", "Backups", "CDN Integration"])

# Offer13 - Web Security Check
OffersDetails37 = OffersDetails.objects.create(offer=Offer13, title="Basic Security Check", revisions=1, delivery_time_in_days=3, price=220, offer_type="basic", features=["Sicherheitsanalyse", "Basis Bericht"])
OffersDetails38 = OffersDetails.objects.create(offer=Offer13, title="Standard Security Check", revisions=2, delivery_time_in_days=4, price=400, offer_type="standard", features=["Sicherheitsanalyse", "Detailbericht", "Empfehlungen"])
OffersDetails39 = OffersDetails.objects.create(offer=Offer13, title="Premium Security Check", revisions=3, delivery_time_in_days=5, price=700, offer_type="premium", features=["Tiefenanalyse", "Schwachstellenbehebung", "Sicherheitsberatung"])

# Offer14 - Website Migration
OffersDetails40 = OffersDetails.objects.create(offer=Offer14, title="Basic Migration", revisions=1, delivery_time_in_days=4, price=300, offer_type="basic", features=["Datenmigration", "Basis Einrichtung"])
OffersDetails41 = OffersDetails.objects.create(offer=Offer14, title="Standard Migration", revisions=2, delivery_time_in_days=5, price=500, offer_type="standard", features=["Datenmigration", "DNS Einrichtung", "Funktionsprüfung"])
OffersDetails42 = OffersDetails.objects.create(offer=Offer14, title="Premium Migration", revisions=3, delivery_time_in_days=7, price=800, offer_type="premium", features=["Komplette Migration", "DNS Einrichtung", "Funktionsprüfung", "Optimierung nach Umzug"])