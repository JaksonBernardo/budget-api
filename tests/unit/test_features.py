import pytest
from api.features.all import UserFeature, SegmentFeature, ClientFeature, SupplierFeature, MaterialFeature

def test_features_enums():
    assert UserFeature.CREATE == "CREATE_USER"
    assert SegmentFeature.CREATE == "CREATE_SEGMENT"
    assert ClientFeature.CREATE == "CREATE_CLIENT"
    assert SupplierFeature.CREATE == "CREATE_SUPPLIER"
    assert MaterialFeature.CREATE == "CREATE_MATERIAL"
