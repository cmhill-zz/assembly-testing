#! /usr/bin/sh

timestamp=`date +%FT%R:%S`
tests=0
failures=0

for tc in testcases/* ; do
    tc=`basename ${tc}`
    sh ./testcases/${tc}/run_test.sh
    return_code=$?

    tests=$((tests + 1))

    if [ ${return_code} -eq 0 ]; then
        echo "<testcase name=\"${tc}\" classname=\"None\">" >> tmp.results
        echo "</testcase>" >> tmp.results
    else
        echo "<testcase name=\"${tc} fail\" classname=\"None\">" >> tmp.results
        echo "<error message=\"Failed\">Failed.</error>" >> tmp.results
        echo "</testcase>" >> tmp.results

        failures=$((failures + 1))
    fi

done

echo "<testsuites>"
echo "<testsuite name=\"Assembler testing\" tests=\"${tests}\" failures=\"${failures}\" timestamp=\"${timestamp}\">"

cat tmp.results

echo "</testsuite>"
echo "</testsuites>"

rm tmp.results