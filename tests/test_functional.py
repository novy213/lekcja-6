from src.manager import Manager
from src.models import Parameters, Transfer


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


def test_get_tax_calculates_tax_on_tenant_income():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=2500.0,
            date='2025-01-04',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-1'
        ),
        Transfer(
            amount_pln=2500.0,
            date='2025-01-05',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-2'
        ),
        Transfer(
            amount_pln=2500.0,
            date='2025-01-06',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-3'
        ),
    ]
    tax = manager.get_tax(2025, 1, 0.085)
    assert tax == 638
    tax = manager.get_tax(2025, 1, 0.10)
    assert tax == 750


def test_check_deposits_verifies_tenant_deposit_payments():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=3000.0,
            date='2025-01-01',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-1'
        ),
        Transfer(
            amount_pln=2900.0,
            date='2025-01-02',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-2'
        ),
        Transfer(
            amount_pln=2800.0,
            date='2025-01-03',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-3'
        ),
    ]
    result = manager.check_deposits()
    assert result['all_deposits_verified'] is True
    assert len(result['verified_deposits']) == 3
    assert result['verified_deposits']['Jan Nowak'] is True
    assert result['verified_deposits']['Adam Kowalski'] is True
    assert result['verified_deposits']['Ewa Adamska'] is True


def test_check_deposits_detects_missing_deposits():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=3000.0,
            date='2025-01-01',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-1'
        ),
        Transfer(
            amount_pln=1500.0,  
            date='2025-01-02',
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-2'
        ),
    ]
    
    result = manager.check_deposits()
    assert result['all_deposits_verified'] is False
    assert result['verified_deposits']['Jan Nowak'] is True
    assert result['verified_deposits']['Adam Kowalski'] is False
    assert result['verified_deposits']['Ewa Adamska'] is False
