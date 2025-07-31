from django.urls import reverse

from wikii.tests import WikiiTests


class EmployeeTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_employee_detail_when_get_by_existing_id_then_returns_it(self):
        existing_id = self.employee_instance_petrov.pk
        response = self.client.get(
            reverse("employee_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["surname"],
                response.data["data"]["name"],
                response.data["data"]["location"],
                response.data["data"]["owner_id"],
            },
            {
                self.employee_instance_petrov.surname,
                self.employee_instance_petrov.name,
                self.employee_instance_petrov.location.pk,
                self.employee_instance_petrov.owner_id,
            },
        )

    def test_get_employee_detail_whe_get_by_non_existing_id_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.get(
            reverse("employee_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_get_employees_list_when_get_wout_filters_then_returns_it(self):
        response = self.client.get(reverse("employees"))

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_employees_list_when_get_by_existing_surname_filter_then_returns_it(
        self,
    ):
        response = self.client.get(reverse("employees"), data={"surname": "Petrov"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["id"], self.employee_instance_petrov.pk
        )

    def test_get_employees_list_when_get_by_existing_name_filter_then_returns_it(self):
        response = self.client.get(reverse("employees"), data={"name": "Arsen"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(
            response.data["data"][0]["id"], self.employee_instance_petrov.pk
        )

    def test_get_employees_list_when_get_by_non_existing_surname_filter_then_returns_empty_list(
        self,
    ):
        response = self.client.get(reverse("employees"), data={"surname": "Sidorov"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_get_employees_list_when_get_by_non_existing_name_filter_then_returns_empty_list(
        self,
    ):
        response = self.client.get(reverse("employees"), data={"name": "Sidor"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_create_employee_when_get_right_data_then_returns_201(self):
        response_before_creating_new_instance = self.client.get(reverse("employees"))
        response_for_creating_new_instance = self.client.post(
            reverse("employees"), data=self.employee_data_good
        )
        response_after_creating_new_instance = self.client.get(reverse("employees"))

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
                response_after_creating_new_instance.data["data"][-1]["surname"],
                response_after_creating_new_instance.data["data"][-1]["name"],
                response_after_creating_new_instance.data["data"][-1]["lastname"],
                response_after_creating_new_instance.data["data"][-1]["place_of_birth"],
                response_after_creating_new_instance.data["data"][-1]["location"],
                response_after_creating_new_instance.data["data"][-1]["owner_id"],
            },
            {
                self.employee_data_good["surname"],
                self.employee_data_good["name"],
                self.employee_data_good["lastname"],
                self.employee_data_good["place_of_birth"],
                self.employee_data_good["location"],
                self.employee_data_good["owner_id"],
            },
        )

    def test_create_employee_when_get_fail_data_then_returns_400(self):
        response_before_creating_new_instance = self.client.get(reverse("employees"))
        response_for_creating_new_instance = self.client.post(
            reverse("employees"), data=self.employee_data_fail
        )
        response_after_creating_new_instance = self.client.get(reverse("employees"))

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

    def test_change_employee_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_id = self.employee_instance_ivanov.pk
        response = self.client.put(
            reverse("employee_by_id", kwargs={"id": existing_id}),
            data=self.employee_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["surname"],
                response.data["data"]["name"],
                response.data["data"]["lastname"],
                response.data["data"]["place_of_birth"],
                response.data["data"]["location"],
                response.data["data"]["owner_id"],
            },
            {
                self.employee_data_good["surname"],
                self.employee_data_good["name"],
                self.employee_data_good["lastname"],
                self.employee_data_good["place_of_birth"],
                self.employee_data_good["location"],
                self.employee_data_good["owner_id"],
            },
        )

    def test_change_employee_when_get_right_data_and_non_existing_instance_then_returns_404(
        self,
    ):
        non_existing_id = 9999
        response = self.client.put(
            reverse("employee_by_id", kwargs={"id": non_existing_id}),
            data=self.employee_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_change_employee_when_get_fail_data_and_existing_instance_then_returns_400(
        self,
    ):
        existing_id = self.employee_instance_petrov.pk
        response = self.client.put(
            reverse("address_by_id", kwargs={"id": existing_id}),
            data=self.employee_data_fail,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_delete_employee_when_get_existing_instance_then_it_deleting_and_returns_204(
        self,
    ):
        existing_id = self.employee_instance_petrov.pk
        response = self.client.delete(
            reverse("employee_by_id", kwargs={"id": existing_id})
        )
        response_after_deleting = self.client.get(
            reverse("employee_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "204 NO DATA"},
        )
        self.assertEqual(
            {
                response_after_deleting.data["status"],
                response_after_deleting.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_delete_employee_when_get_non_existing_instance_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.delete(
            reverse("employee_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )


class EmployeePositionTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_employeeposition_detail_when_get_by_existing_id_then_returns_it(self):
        existing_composite_id = {
            "position_id": self.position_instance_math_teacher_of_study_center.pk,
            "employee_id": self.employee_instance_petrov.pk,
        }

        response = self.client.get(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs=existing_composite_id,
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["employee_id"],
                response.data["data"]["position_id"],
                response.data["data"]["owner_id"],
            },
            {
                self.employeeposition_instance_petrov_math_teacher.employee_id.pk,
                self.employeeposition_instance_petrov_math_teacher.position_id.pk,
                self.employeeposition_instance_petrov_math_teacher.owner_id,
            },
        )

    def test_get_employeeposition_detail_when_get_by_non_existing_employee_id_then_returns_404(
        self,
    ):
        non_existing_composite_id = {
            "position_id": self.position_instance_math_teacher_of_study_center.pk,
            "employee_id": 9999,
        }
        response = self.client.get(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs=non_existing_composite_id,
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_get_employeeposition_detail_when_get_by_non_existing_position_id_then_returns_404(
        self,
    ):
        non_existing_composite_id = {
            "position_id": 9999,
            "employee_id": self.employee_instance_petrov.pk,
        }
        response = self.client.get(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs=non_existing_composite_id,
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )

    def test_get_employeeposition_detail_when_get_employee_is_not_on_this_position_then_returns_404(
        self,
    ):
        non_existing_composite_id = {
            "position_id": self.position_instance_master_of_study_center.pk,
            "employee_id": self.employee_instance_petrov.pk,
        }
        response = self.client.get(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs=non_existing_composite_id,
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. This Employee is not on this Position."},
        )

    def test_get_employeepositions_list_when_get_existing_employee_id_then_returns_it(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        response = self.client.get(
            reverse(
                "positions_by_employee_id",
                kwargs={"employee_id": existing_employee_id},
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_employeeposition_list_when_get_non_existing_employee_id_then_returns_404(
        self,
    ):
        non_existing_employee_id = 9999
        response = self.client.get(
            reverse(
                "positions_by_employee_id",
                kwargs={"employee_id": non_existing_employee_id},
            )
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_create_employeeposition_when_get_right_data_then_returns_201(self):
        existing_employee_id = self.employee_instance_petrov.pk

        response_before_creating_new_instance = self.client.get(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            )
        )
        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            ),
            data=self.employeeposition_data_good,
        )
        response_after_creating_new_instance = self.client.get(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            )
        )

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

    def test_create_employeeposition_when_get_existing_employee_id_wout_position_id_then_returns_400(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk

        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            ),
            data=self.employeeposition_data_fail_wout_position_id,
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Missing required field: position_id."},
        )

    def test_create_employeeposition_when_get_non_existing_employee_id_and_existing_position_id_then_returns_404(
        self,
    ):
        non_existing_employee_id = 9999

        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id",
                kwargs={"employee_id": non_existing_employee_id},
            ),
            data=self.employeeposition_data_good,
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_create_employeeposition_when_get_non_existing_position_id_and_existing_employee_id_then_returns_404(
        self,
    ):
        existing_employee_id = self.employee_instance_ivanov.pk

        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            ),
            data=self.employeeposition_data_fail_non_existing_position_id,
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )

    def test_create_employeeposition_when_get_existing_employee_id_and_existing_position_id_but_employee_already_assigned_to_this_position_then_returns_400(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk
        data_already_assigned_employeeposition = {
            "position_id": existing_position_id,
            "owner_id": "OWNER_ID",
        }

        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            ),
            data=data_already_assigned_employeeposition,
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Employee already assigned to this position."},
        )

    def test_create_employeeposition_when_get_existing_employee_id_and_existing_position_id_who_are_not_assigned_but_wout_owner_id_then_returns_400(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_master_of_study_center.pk
        data_not_assigned_employeeposition = {"position_id": existing_position_id}

        response_for_creating_new_instance = self.client.post(
            reverse(
                "positions_by_employee_id", kwargs={"employee_id": existing_employee_id}
            ),
            data=data_not_assigned_employeeposition,
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_change_employeeposition_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk

        response = self.client.put(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": existing_position_id,
                },
            ),
            data=self.employeeposition_data_good_with_finish_date,
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"OK", "200 OK"},
        )

    def test_change_employeeposition_when_get_fail_data_and_existing_instance_then_returns_400(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk

        response = self.client.put(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": existing_position_id,
                },
            ),
            data=self.employeeposition_data_fail_wout_owner_id,
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_change_employeeposition_when_get_right_data_and_non_existing_employee_id_then_returns_404(
        self,
    ):
        non_existing_employee_id = 9999
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk

        response = self.client.put(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": non_existing_employee_id,
                    "position_id": existing_position_id,
                },
            ),
            data=self.employeeposition_data_good,
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_change_employeeposition_when_get_right_data_and_non_existing_position_id_then_returns_404(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        non_existing_position_id = 9999

        response = self.client.put(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": non_existing_position_id,
                },
            ),
            data=self.employeeposition_data_good,
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )

    def test_change_employeeposition_when_get_existing_employee_id_and_position_id_but_employee_dont_assigned_to_this_position_then_returns_404(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_master_of_study_center.pk

        response = self.client.put(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": existing_position_id,
                },
            ),
            data=self.employeeposition_data_good,
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. This Employee is not on this Position."},
        )

    def test_delete_employeeposition_when_get_existing_instance_then_returns_204(self):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk

        response = self.client.delete(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": existing_position_id,
                },
            )
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"OK", "204 NO DATA"},
        )

    def test_delete_employeeposition_when_get_non_existing_employee_id_and_existing_position_id_then_returns_404(
        self,
    ):
        non_existing_employee_id = 9999
        existing_position_id = self.position_instance_math_teacher_of_study_center.pk

        response = self.client.delete(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": non_existing_employee_id,
                    "position_id": existing_position_id,
                },
            )
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Employee was not found."},
        )

    def test_delete_employeeposition_when_get_non_existing_position_id_and_existing_employee_id_then_returns_404(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        non_existing_position_id = 9999

        response = self.client.delete(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": non_existing_position_id,
                },
            )
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )

    def test_delete_employeeposition_when_get_existing_employee_id_and_existing_position_id_but_employee_not_assigned_to_this_position_then_returns_404(
        self,
    ):
        existing_employee_id = self.employee_instance_petrov.pk
        existing_position_id = self.position_instance_master_of_study_center.pk

        response = self.client.delete(
            reverse(
                "position_by_employee_id_and_position_id",
                kwargs={
                    "employee_id": existing_employee_id,
                    "position_id": existing_position_id,
                },
            )
        )
        self.assertEqual(
            {
                response.data["status"],
                response.data["message"],
            },
            {"ERROR", "404 Not Found. This Employee is not on this Position."},
        )
