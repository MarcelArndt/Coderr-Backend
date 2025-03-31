from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profiles, Offers, OffersDetails  
from rest_framework.authtoken.models import Token

# Create your tests here.


class OfferCreateTestCase(APITestCase):
    def setUp(self):
        # Nutzer und Profil erstellen
        self.user = User.objects.create_user(username="Haru", password="testpassword")
        self.profile = Profiles.objects.create(user=self.user)

        self.client.login(username="Haru", password="testpassword")  # Falls Session-Auth genutzt wird
        token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.offers = []
        self.URL = "/api/offers/"

        self.offer_data = [
            {
                "title": "Website-Design Paket",
                "description": "Individuelles Webdesign für kleine Unternehmen",
                "min_price": "250",
                "min_delivery_time": 7,
                "details": [
                    {
                        "title": "Basic Design",
                        "revisions": 1,
                        "delivery_time_in_days": 5,
                        "price": "300.00",
                        "offer_type": "Basic",
                        "features": {"responsive": "Ja", "seo_optimized": "Nein"}
                    }
                ]
            },
            {
                "title": "Logo Erstellung",
                "description": "Professionelles Logo für deine Marke",
                "min_price": "80",
                "min_delivery_time": 3,
                "details": [
                    {
                        "title": "Premium Logo",
                        "revisions": 3,
                        "delivery_time_in_days": 2,
                        "price": "120.00",
                        "offer_type": "Premium",
                        "features": {"vector_format": "Ja", "color_variations": "Ja"}
                    }
                ]
            },
            {
                "title": "SEO Optimierung",
                "description": "Verbesserung des Google-Rankings durch gezielte Maßnahmen und SEO Optimierung",
                "min_price": "500",
                "min_delivery_time": 10,
                "details": [
                    {
                        "title": "Komplette SEO Analyse",
                        "revisions": 2,
                        "delivery_time_in_days": 7,
                        "price": "750.00",
                        "offer_type": "Advanced",
                        "features": {"keyword_research": "Ja", "backlink_analysis": "Ja"}
                    }
                ]
            },
            {
                "title": "Social Media Betreuung",
                "description": "Tägliche Pflege und Optimierung von Social Media Kanälen",
                "min_price": "200",
                "min_delivery_time": 4,
                "details": [
                    {
                        "title": "Social Media Boost",
                        "revisions": 1,
                        "delivery_time_in_days": 3,
                        "price": "250.00",
                        "offer_type": "Standard",
                        "features": {"content_creation": "Ja", "community_management": "Nein"}
                    }
                ]
            }
        ]
        
        for each in self.offer_data:
            details_data = each.pop("details", [])  # Details vorübergehend entfernen
            offer = Offers.objects.create(user=self.profile, **each)
            for detail in details_data:
                offer_detail = OffersDetails.objects.create(offer=offer, **detail)
            offer.save()
            self.offers.append(offer)



    def test_create_offer(self):
        new_data = {
                    "title": "App-Entwicklung",
                    "description": "Entwicklung einer mobilen App für iOS und Android",
                    "min_price": "1500",
                    "min_delivery_time": 15,
                    "details": [
                        {
                            "title": "Basis-App",
                            "revisions": 2,
                            "delivery_time_in_days": 12,
                            "price": "1800.00",
                            "offer_type": "Standard",
                            "features": {"ios_version": "Ja", "android_version": "Ja", "push_notifications": "Ja"}
                        }
                    ]
                }
        response = self.client.post(self.URL, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
 
    def test_get_response(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_response(self):
        offer = self.offers[0]
        response = self.client.get(f"/api/offers/{offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    '''
    def test_search_offer(self):
        response = self.client.get(f"{self.URL}?search=SEO")
        print(r"{self.URL}?search=SEO")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        print(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "SEO Optimierung")



    def test_filter_min_price(self):
        response = self.client.get("/api/offers/?min_price=250")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        print(results)
    '''     
    '''      
    def test_filter_max_delivery_time(self):
        response = self.client.get("/api/offers/?max_delivery_time=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertTrue(all(offer["min_delivery_time"] <= 5 for offer in results))
        print("Test: max_delivery_time was successfuly")
    
    def test_ordering_by_price(self):
        response = self.client.get("/api/offers/?ordering=min_price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        prices = [float(offer["min_price"]) for offer in results]
        self.assertEqual(prices, sorted(prices))
        print("Test: ordering_by_price was successfuly")
    '''
    def test_filter_by_creator_id(self):
        response = self.client.get(f"/api/offers/?creator_id={self.profile.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        self.assertTrue(all(offer["username"] == self.user.username for offer in results))
        print("Test: filter_by_creator_id was successfuly")
