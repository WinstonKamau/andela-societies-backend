#!/usr/bin/env bash

set -o errexit
set -o pipefail


declare_env_variables() {

  # Declaring environment variables
  #
  # Some environment variables assigned externally are:
  # SLACK_CHANNEL_HOOK : This is the webhook for the Slack App where notifications will be sent from
  # DEPLOYMENT_CHANNEL : This is the channel on which the Slack notifications will be posted
  # MESSAGE_TEXT: The text to be sent to the slack channel
  # Some template for the Slack message

  MESSAGE_COLOR="$2"

  case "$MESSAGE_COLOR" in
    good)
      MESSAGE_STATUS="was upgraded successfully"
        ;;
    danger)
      MESSAGE_STATUS="upgrade failed!!!"
        ;;
    *)
        echo "Err: Wrong argument provided for the message color."
        exit 1
        ;;
  esac

  case "$1" in
    master)
      MESSAGE_TEXT="Production database $MESSAGE_STATUS"
        ;;
    develop)
      MESSAGE_TEXT="Staging database $MESSAGE_STATUS"
        ;;
    *)
      MESSAGE_TEXT="Wrong branch *$1* provided for upgrading the database."
      MESSAGE_COLOR="danger"
        ;;
  esac
  

  COMMIT_LINK="https://github.com/${CIRCLE_PROJECT_USERNAME}/${CIRCLE_PROJECT_REPONAME}/commit/${CIRCLE_SHA1}"
  IMG_TAG="$(git rev-parse --short HEAD)"
  CIRCLE_WORKFLOW_URL="https://circleci.com/workflow-run/${CIRCLE_WORKFLOW_ID}"
  SLACK_TEXT_TITLE="CircleCI Build #$CIRCLE_BUILD_NUM"
  SLACK_DEPLOYMENT_TEXT="Executed Git Commit <$COMMIT_LINK|${IMG_TAG}>: ${MESSAGE_TEXT}"
}

send_notification() {

  # Sending the Slack notification

  curl -X POST --data-urlencode \
  "payload={
      \"channel\": \"${DEPLOYMENT_CHANNEL}\",
      \"username\": \"JobNotification\",
      \"attachments\": [{
          \"fallback\": \"CircleCI job notification\",
          \"color\": \"${MESSAGE_COLOR}\",
          \"author_name\": \"Branch: $CIRCLE_BRANCH by ${CIRCLE_USERNAME}\",
          \"author_link\": \"https://github.com/AndelaOSP/andela-societies-backend/tree/${CIRCLE_BRANCH}\",
          \"title\": \"${SLACK_TEXT_TITLE}\",
          \"title_link\": \"$CIRCLE_WORKFLOW_URL\",
          \"text\": \"${SLACK_DEPLOYMENT_TEXT}\"
      }]
  }" \
  "${SLACK_CHANNEL_HOOK}"
}

main() {
  echo "Declaring environment variables"
  declare_env_variables "$@"

  echo "Sending notification"
  send_notification
}

main "$@"
