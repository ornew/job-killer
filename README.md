# JobKiller

Kubernetes Custom Controller

ジョブ絶対殺すマン

`job-killer: kill-me`

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-job
  labels:
    job-killer: kill-me
spec:
  parallelism: 1
  template:
    spec:
      containers:
      - name: test-job
        image: hello-world
      restartPolicy: Never
```
