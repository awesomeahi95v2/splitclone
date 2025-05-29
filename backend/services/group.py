from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from models import GroupModel
from backend.db import db
from models import GroupMembership

class GroupService:
    @staticmethod
    def create_group(name, created_by_user_id):
        group = GroupModel(name=name, created_by=created_by_user_id)
        db.session.add(group)
        db.session.commit()

        membership = GroupMembership(
            group_id=group.id,
            user_id=created_by_user_id,
            role='admin',
            status='joined'
        )
        db.session.add(membership)
        db.session.commit()
        
        return group

    @staticmethod
    def get_group(group_id):
        return GroupModel.query.get(group_id)

    @staticmethod
    def get_groups_by_user(user):
        return [
            membership.group
            for membership in user.memberships
            if membership.status == "joined"
        ]

    @staticmethod
    def settle_up(group_id):
        group = GroupModel.query.get(group_id)
        if not group:
            raise ValueError("Group not found")
        
        balances = defaultdict(float)

        for expense in group.expenses:
            payer = expense.paid_by
            balances[payer] += float(expense.amount)

            for split in expense.splits:
                balances[split.user_id] -= float(split.amount)

        for user in balances:
            balances[user] = float(Decimal(balances[user]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))        

        debtors = []
        creditors = []

        for user, balance in balances.items():
            if balance < -0.01:
                debtors.append((user, balance))
            elif balance > 0.01:
                creditors.append((user, balance))

        debtors.sort(key=lambda x:x[1])
        creditors.sort(key=lambda x: x[1], reverse=True)

        transactions = []

        i = 0
        j = 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt_amt = debtors[i]
            creditor, credit_amt = creditors[j]

            transfer_amt = min(-debt_amt, credit_amt)
            transfer_amt = float(Decimal(transfer_amt).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

            transactions.append({
                "from": debtor,
                "to": creditor,
                "amount": transfer_amt
            })

            debtors[i] = (debtor, debt_amt + transfer_amt)
            creditors[j] = (creditor, credit_amt - transfer_amt)

            if abs(debtors[i][1]) < 0.01:
                i += 1
            if abs(creditors[j][1]) < 0.01:
                j += 1

        return transactions
