#!/bin/sh
grep -rli '/sys/kernel/debug/tracing' /bcc-master | xargs -i@ sed -i 's/\/sys\/kernel\/debug\/tracing/\/sys\/kernel\/tracing/g' @