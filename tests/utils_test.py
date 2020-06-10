import json
import logging

import pytest
from app.utils import TransformationHelper
from tests.fixtures.payloads import enterprise_attack_pattern


def test_retrieve_simple_paths():
    expected_result = {'type': 'bundle', 'spec_version': '2.0'}
    attrs_to_find = ['type', 'spec_version']
    data = enterprise_attack_pattern
    result = TransformationHelper.get_mapped_attributes(data, attrs_to_find)
    assert result == expected_result


def test_retrieve_nested_paths():
    expected_result = {
        'type': 'bundle',
        'spec_version': '2.0',
        'some_nested.some_nested_child': 'it works'
    }
    attrs_to_find = ['type', 'spec_version', 'some_nested.some_nested_child']
    data = enterprise_attack_pattern
    result = TransformationHelper.get_mapped_attributes(data, attrs_to_find)
    assert result == expected_result


def test_retrieve_indexed_paths():
    expected_result = {
        'objects[0].name': 'Inhibit System Recovery',
        'objects[0].x_mitre_permissions_required[0]': 'Administrator'
    }
    attrs_to_find = [
        'objects[0].name', 'objects[0].x_mitre_permissions_required[0]'
    ]
    data = enterprise_attack_pattern
    result = TransformationHelper.get_mapped_attributes(data, attrs_to_find)
    assert result == expected_result


def test_retrieve_mixed_paths():
    expected_result = {
        'type': 'bundle',
        'some_nested.some_nested_child': 'it works',
        'objects[0].x_mitre_permissions_required[0]': 'Administrator',
        'objects[0].kill_chain_phases[0]': {
            "kill_chain_name": "mitre-attack",
            "phase_name": "impact"
        }
    }
    attrs_to_find = [
        'type', 'some_nested.some_nested_child',
        'objects[0].x_mitre_permissions_required[0]',
        'objects[0].kill_chain_phases[0]'
    ]
    data = enterprise_attack_pattern
    result = TransformationHelper.get_mapped_attributes(data, attrs_to_find)
    assert result == expected_result


def test_retrieve_wrong_paths():
    expected_result = {'type': 'bundle'}
    attrs_to_find = [
        'type', 'some_wrong.some_nested_child', 'this.is.not.ok', 'thisneither'
    ]
    data = enterprise_attack_pattern
    result = TransformationHelper.get_mapped_attributes(data, attrs_to_find)
    assert result == expected_result
