import pytest

from build.lib.envoy_schema.server.schema.sep2.end_device import AbstractDevice
from envoy_schema.server.schema.sep2.identification import Resource
from envoy_schema.server.schema.sep2.primitive_types import UriFullyQualified, UriWithoutHost
from envoy_schema.server.schema.sep2.pub_sub import (
    ConditionAttributeIdentifier,
    Notification,
    NotificationStatus,
    Subscription,
    SubscriptionEncoding,
)


def test_subscription():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/subscription.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_sub: Subscription = Subscription.from_xml(raw_xml)

    assert parsed_sub.subscribedResource == "/upt/0/mr/4/r"
    assert type(parsed_sub.subscribedResource) == UriWithoutHost
    assert parsed_sub.encoding == SubscriptionEncoding.XML
    assert parsed_sub.level == "+S1"
    assert parsed_sub.limit == 1
    assert parsed_sub.notificationURI == "http://example.com:8001/note"
    assert type(parsed_sub.notificationURI) == UriFullyQualified
    assert parsed_sub.condition is None


def test_subscription_no_relative_uri():
    """Checks that validation disallows relative notification uris"""

    # load as per normal but change the URI
    with open("tests/data/subscription.xml", "r") as fp:
        raw_xml = fp.read()
    raw_xml = raw_xml.replace("http://example.com:8001/note", "/invalid/relative/uri")
    with pytest.raises(ValueError):
        Subscription.from_xml(raw_xml)


def test_subscription_conditions():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/subscription_condition.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_sub: Subscription = Subscription.from_xml(raw_xml)

    assert parsed_sub.subscribedResource == "/upt/0/mr/4/r"
    assert type(parsed_sub.subscribedResource) == UriWithoutHost
    assert parsed_sub.encoding == SubscriptionEncoding.XML
    assert parsed_sub.level == "+S1"
    assert parsed_sub.limit == 1
    assert parsed_sub.notificationURI == "http://example.com:8001/note"
    assert type(parsed_sub.notificationURI) == UriFullyQualified
    assert parsed_sub.condition is not None
    assert parsed_sub.condition.lowerThreshold == 100
    assert parsed_sub.condition.upperThreshold == 200
    assert parsed_sub.condition.attributeIdentifier == ConditionAttributeIdentifier.READING_VALUE


def test_notification():
    """Simple validation to ensure we can read basic XML"""
    with open("tests/data/notification.xml", "r") as fp:
        raw_xml = fp.read()

    parsed_notif: Notification = Notification.from_xml(raw_xml)

    assert parsed_notif.subscribedResource == "/upt/0/mr/4/r"
    assert parsed_notif.resource is not None
    assert type(parsed_notif.resource) == Resource
    assert parsed_notif.status == NotificationStatus.DEFAULT
    assert parsed_notif.subscriptionURI == "/edev/8/sub/5"
    assert type(parsed_notif.subscriptionURI) == UriWithoutHost


def test_notification_encode_abstract_device():
    """Can AbstractDevice - a descendent of Resource be encoded in a notification?"""

    with open("tests/data/notification.xml", "r") as fp:
        raw_xml = fp.read()

    notif: Notification = Notification.from_xml(raw_xml)
    notif.resource = AbstractDevice.validate({"lFDI": "lfdi-123", "sFDI": "456", "href": "my-device-789"})

    xml_result = Notification.to_xml(notif, skip_empty=True).decode()
    assert "lfdi-123" not in xml_result, "Only the Resource parts of the schema should encode"
    assert "456" not in xml_result, "Only the Resource parts of the schema should encode"
    assert 'href="my-device-789"' in xml_result
