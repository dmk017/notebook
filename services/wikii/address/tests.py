from django.urls import reverse
from wikii.tests import WikiiTests


class CountryTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_country_detail_when_get_by_existing_id_then_returns_it(self):
        response = self.client.get(
            reverse("country_by_id", kwargs={"id": self.country_instance_russia.pk})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )

        self.assertEqual(
            {response.data["data"]["id"], response.data["data"]["name"]},
            {self.country_instance_russia.pk, self.country_instance_russia.name},
        )

    def test_get_country_detail_when_get_by_non_existing_id_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.get(
            reverse("country_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Country was not found."},
        )

    def test_get_countries_list_when_get_wout_name_filter_then_returns_two_items(self):
        response = self.client.get(reverse("countries"))

        self.assertEqual(len(response.data["data"]), 2)
        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {response.data["data"][0]["name"], response.data["data"][1]["name"]},
            {self.country_instance_france.name, self.country_instance_russia.name},
        )

    def test_get_countries_list_when_get_by_existing_name_filter_then_returns_it(
        self,
    ):
        response = self.client.get(reverse("countries"), data={"name": "Russia"})

        self.assertEqual(
            {response.data["status"], response.data["message"]}, {"OK", "200 OK"}
        )
        self.assertEqual(
            response.data["data"][0]["name"],
            self.country_instance_russia.name,
        )

    def test_get_countries_list_when_get_by_non_existing_name_filter_then_returns_empty_list(
        self,
    ):
        response = self.client.get(reverse("countries"), data={"name": "Iceland"})

        self.assertEqual(
            {response.data["status"], response.data["message"]}, {"OK", "200 OK"}
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_create_country_when_get_right_data_then_returns_201(self):
        response_before_creating_new_instance = self.client.get(reverse("countries"))
        response_for_creating_new_instance = self.client.post(
            reverse("countries"), data=self.country_data_good
        )
        response_after_creating_new_instance = self.client.get(reverse("countries"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"OK", "201 CREATED"},
        )
        self.assertEqual(
            1 + len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )
        self.assertEqual(
            response_after_creating_new_instance.data["data"][-1]["name"],
            "UK",
        )

    def test_create_country_when_get_fail_data_then_returns_400(self):
        response_before_creating_new_instance = self.client.get(reverse("countries"))
        response_for_creating_new_instance = self.client.post(
            reverse("countries"), data=self.country_data_fail
        )
        response_after_creating_new_instance = self.client.get(reverse("countries"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )
        self.assertEqual(
            len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )


class AddressTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_address_detail_when_get_by_existing_id_then_returns_it(self):
        existing_id = self.address_instance_red_square.pk
        response = self.client.get(
            reverse("address_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["id"],
                response.data["data"]["street"],
                response.data["data"]["city"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
                response.data["data"]["created_at"],
                response.data["data"]["is_deleted"],
                response.data["data"]["country"],
            },
            {
                self.address_instance_red_square.pk,
                self.address_instance_red_square.street,
                self.address_instance_red_square.city,
                self.address_instance_red_square.description,
                self.address_instance_red_square.owner_id,
                str(self.address_instance_red_square.created_at),
                self.address_instance_red_square.is_deleted,
                self.address_instance_red_square.country.pk,
            },
        )

    def test_get_address_detail_when_get_by_non_existing_id_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.get(
            reverse("address_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Address was not found."},
        )

    def test_get_addresses_list_when_get_wout_name_filter_then_returns_two_items(self):
        response = self.client.get(reverse("addresses"))

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_addresses_list_when_get_by_existing_street_filter_then_returns_it(
        self,
    ):
        response = self.client.get(
            reverse("addresses"), data={"street": "Красная площадь"}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            response.data["data"][0]["id"], self.address_instance_red_square.pk
        )

    def test_get_addresses_list_when_get_by_existing_city_filter_then_returns_it(
        self,
    ):
        response = self.client.get(reverse("addresses"), data={"city": "Москва"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            response.data["data"][0]["id"], self.address_instance_red_square.pk
        )

    def test_get_addresses_list_when_get_by_non_existing_street_filter_then_returns_empty_list(
        self,
    ):
        non_existing_street = "Староватутинский проезд"
        response = self.client.get(
            reverse("addresses"), data={"street": non_existing_street}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_get_addresses_list_when_get_by_non_existing_city_filter_then_returns_empty_list(
        self,
    ):
        non_existing_city = "Орел"
        response = self.client.get(
            reverse("addresses"), data={"street": non_existing_city}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_create_address_when_get_right_data_then_returns_201(self):
        response_before_creating_new_instance = self.client.get(reverse("addresses"))
        response_for_creating_new_instance = self.client.post(
            reverse("addresses"), data=self.address_data_good
        )
        response_after_creating_new_instance = self.client.get(reverse("addresses"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"OK", "201 CREATED"},
        )
        self.assertEqual(
            1 + len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )
        self.assertEqual(
            {
                response_after_creating_new_instance.data["data"][-1]["street"],
                response_after_creating_new_instance.data["data"][-1]["city"],
                response_after_creating_new_instance.data["data"][-1]["country"],
                response_after_creating_new_instance.data["data"][-1]["description"],
                response_after_creating_new_instance.data["data"][-1]["owner_id"],
            },
            {
                self.address_data_good["street"],
                self.address_data_good["city"],
                self.address_data_good["country"],
                self.address_data_good["description"],
                self.address_data_good["owner_id"],
            },
        )

    def test_create_address_when_get_fail_data_then_returns_400(self):
        response_before_creating_new_instance = self.client.get(reverse("addresses"))
        response_for_creating_new_instance = self.client.post(
            reverse("addresses"), data=self.address_data_fail
        )
        response_after_creating_new_instance = self.client.get(reverse("addresses"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )
        self.assertEqual(
            len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )

    def test_change_address_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_id = self.address_instance_red_square.pk
        response = self.client.put(
            reverse("address_by_id", kwargs={"id": existing_id}),
            data=self.address_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["street"],
                response.data["data"]["city"],
                response.data["data"]["country"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
            },
            {
                self.address_data_good["street"],
                self.address_data_good["city"],
                self.address_data_good["country"],
                self.address_data_good["description"],
                self.address_data_good["owner_id"],
            },
        )

    def test_change_address_when_get_right_data_and_non_existing_instance_then_returns_404(
        self,
    ):
        non_existing_id = 9999
        response = self.client.put(
            reverse("address_by_id", kwargs={"id": non_existing_id}),
            data=self.address_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Address was not found."},
        )

    def test_change_address_when_get_fail_data_and_existing_instance_then_returns_400(
        self,
    ):
        existing_id = self.address_instance_red_square.pk
        response = self.client.put(
            reverse("address_by_id", kwargs={"id": existing_id}),
            data=self.address_data_fail,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_delete_address_when_get_existing_instance_then_it_deleting_and_returns_204(
        self,
    ):
        existing_id = self.address_instance_red_square.pk
        response = self.client.delete(
            reverse("address_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "204 NO DATA"},
        )

    def test_delete_address_when_get_non_existing_instance_then_returns_404(self):
        non_existing_primary_key = 9999
        response = self.client.delete(
            reverse("address_by_id", kwargs={"id": non_existing_primary_key})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Address was not found."},
        )
