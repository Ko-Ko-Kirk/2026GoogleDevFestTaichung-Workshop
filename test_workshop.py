from copy import deepcopy
import unittest
from workshop import EXAMPLES, Blocked, local_expense, read_json, verify_tools
from devfest_security.policy import authorize

class ExpenseWorkshopTests(unittest.TestCase):
    def test_owner_reads_own_expense(self):
        self.assertEqual(local_expense('EXP-ALICE')['amount'], 120)

    def test_colleague_cannot_read(self):
        with self.assertRaises(Blocked):
            local_expense('EXP-BOB')

    def test_manager_cannot_approve_cross_tenant(self):
        with self.assertRaises(Blocked):
            authorize('bob', 'approve_expense', {'expense_id': 'EXP-OTHER'})

    def test_ordinary_description_change_needs_review(self):
        approved = read_json(EXAMPLES / 'approved-tools.json')
        verify_tools(deepcopy(approved), approved)
        candidate = deepcopy(approved)
        candidate['tools'][0]['description'] = '查詢報帳進度。'
        with self.assertRaises(Blocked):
            verify_tools(candidate, approved)
