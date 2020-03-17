import pulumi
from isodate import Duration, duration_isoformat
from pulumi_azure import core, cosmosdb, appservice, storage, servicebus

# Create an Azure Resource Group
resource_group = core.ResourceGroup(
    'messaging-samples',
    location='EastUs',
    name='messaging-samples')

# Create an Azure Service Bus namespace
sbnamespace = servicebus.Namespace('ns-messaging-samples',
                                   sku='Standard',
                                   name='ns-messaging-samples',
                                   location='EastUs',
                                   resource_group_name=resource_group.name
                                   )

# Create an associated queue within the above namespace
servicebus.Queue('simplequeue',
                 name='simplequeue',
                 namespace_name=sbnamespace.name,
                 dead_lettering_on_message_expiration=True,
                 resource_group_name=resource_group.name,
                 max_size_in_megabytes=1024,
                 default_message_ttl=duration_isoformat(Duration(days=5))
                 )

# Create an associated topic within the above namespace
simpletopic = servicebus.Topic('simpletopic',
                               name='simpletopic',
                               resource_group_name=resource_group.name,
                               namespace_name=sbnamespace.name,
                               max_size_in_megabytes=1024,
                               status='Active'
                               )

servicebus.Subscription('all_messages',
                        name='all_messages',
                        resource_group_name=resource_group.name,
                        namespace_name=sbnamespace.name,
                        max_delivery_count=5,
                        dead_lettering_on_message_expiration=True,
                        default_message_ttl=duration_isoformat(
                            Duration(days=5)),
                        requires_session=False,
                        topic_name=simpletopic.name)

filtered_messages = servicebus.Subscription('filtered_messages',
                                            name='filtered_messages',
                                            resource_group_name=resource_group.name,
                                            namespace_name=sbnamespace.name,
                                            max_delivery_count=5,
                                            dead_lettering_on_message_expiration=True,
                                            default_message_ttl=duration_isoformat(
                                                Duration(days=5)),
                                            requires_session=False,
                                            topic_name=simpletopic.name)

servicebus.SubscriptionRule('content_filter',
                            name='content_filter',
                            topic_name=simpletopic.name,
                            subscription_name=filtered_messages.name,
                            resource_group_name=resource_group.name,
                            namespace_name=sbnamespace.name,
                            filter_type='CorrelationFilter',
                            correlation_filter={
                                'content_type': 'application/json',
                                # 'label': 'content'
                            })

# Create sender and receiver access policies
receiverKey = servicebus.NamespaceAuthorizationRule('RootReceiverAccessKey',
                                                    listen=True,
                                                    send=False,
                                                    namespace_name=sbnamespace.name,
                                                    resource_group_name=resource_group.name,
                                                    name='RootReceiverAccessKey')

senderKey = servicebus.NamespaceAuthorizationRule('RootSenderAccessKey',
                                                  listen=False,
                                                  send=True,
                                                  namespace_name=sbnamespace.name,
                                                  resource_group_name=resource_group.name,
                                                  name='RootSenderAccessKey')


# Export the connection string for the storage account
pulumi.export('namespace_id', sbnamespace.id)
pulumi.export('namespace_name', sbnamespace.name)
pulumi.export('sender connection string', senderKey.primary_connection_string)
pulumi.export('receiver connection string',
              receiverKey.primary_connection_string)
