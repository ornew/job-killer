
import os
import json

import requests

from kubernetes import client, config, watch

def notif2slack(namespace, name, start_time, completion_time, duration, failed, succeeded):
  if 'SLACK_WEBHOOK_URL' in os.environ:
    url = os.environ['SLACK_WEBHOOK_URL']
    payloads = {
      'username':'JobKiller',
      'text': '`{}/{}` is completed.'.format(namespace, name),
      'fields': [
        {
          'title': 'Start Time',
          'value': start_time,
          'short': True,
        },
        {
          'title': 'Completion Time',
          'value': completion_time,
          'short': True,
        },
        {
          'title': 'Duration',
          'value': '{}s'.format(duration),
        },
        {
          'title': 'Failed',
          'value': failed,
          'short': True,
        },
        {
          'title': 'Succeeded',
          'value': succeeded,
          'short': True,
        },
      ],
    }
    res = requests.post(url, data=json.dumps(payloads))
    if res.status_code != 200:
      print('failed send notif to slack: {}'.format(res.text))

LABEL_SELECTOR = 'job-killer=kill-me'

if __name__ == '__main__':
  if 'KUBERNETES_PORT' in os.environ:
    config.load_incluster_config()
  else:
    config.load_kube_config()

  v1 = client.BatchV1Api()
  # this program is not handle exception :D lol
  while True:
    stream = watch.Watch().stream(
      v1.list_job_for_all_namespaces,
      label_selector=LABEL_SELECTOR)
    for event in stream:
      obj  = event['object']
      typ  = event['type']
      name = obj.metadata.name
      ns   = obj.metadata.namespace
      stat = obj.status
      print('{}/{} is {}.'.format(ns, name, typ))  # debug log
      if obj.metadata.deletion_timestamp is not None:
        # already deleted
        continue
      if typ != 'MODIFIED':
        # ignore ADDED, DELETED
        continue
      if stat.completion_time is not None:
        duration = (stat.completion_time - stat.start_time).total_seconds()
        # job is completed
        notif2slack(
          namespace       = ns,
          name            = name,
          start_time      = stat.start_time.strftime('%Y-%m-%d %H:%M:%S'),
          completion_time = stat.completion_time.strftime('%Y-%m-%d %H:%M:%S'),
          duration        = duration,
          failed          = stat.failed,
          succeeded       = stat.succeeded,
        )
        print('{}/{} is COMPLETED. try deleting...'.format(ns,name)) # debug log
        body = client.V1DeleteOptions(propagation_policy='Foreground')
        _ = v1.delete_namespaced_job(name, ns, body)
