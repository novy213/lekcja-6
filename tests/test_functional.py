from src.manager import Manager
from src.models import Parameters


def test_apartment_settlement_total_due_matches_tenants_total_due():
    manager = Manager(Parameters())
    apartment_key = 'apart-polanka'
    year = 2025
    month = 1

    apartment_settlement = manager.get_settlement(apartment_key, year, month)
    assert apartment_settlement is not None

    tenant_settlements = manager.create_tenants_settlements(apartment_settlement)
    assert isinstance(tenant_settlements, list)
    assert len(tenant_settlements) > 0

    total_due_from_tenants = sum(ts.total_due_pln for ts in tenant_settlements)

    assert total_due_from_tenants == apartment_settlement.total_due_pln
    assert total_due_from_tenants == manager.get_apartment_costs(apartment_key, year, month)
