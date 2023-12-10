node {
    def SKIP_PROD = true;

    docker.image('python:2-alpine').inside {
        stage('Build') {
            checkout scm
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
        }
    }
    docker.image('qnib/pytest').inside {
        stage('Test') {
            checkout scm
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            junit 'test-reports/results.xml'
        }
    }

    def approve
    stage("Approval") {
        try {
            timeout(time: 20, unit: 'SECONDS') {
                approve = input(message: 'Lanjutkan ke tahap Deploy?', ok: 'Yes')
            }
        } catch (Throwable e) {
            approve = "No"
            echo "Approval ignored"
        }
        echo approve
    }
    
    if (approve == 'Yes') {
        stage('Deploy') {
            checkout scm
            sh 'docker run --rm -v $(pwd)/sources:/src cdrx/pyinstaller-linux:python2 \'pyinstaller -F add2vals.py\''
            archiveArtifacts 'sources/dist/add2vals'
        }
    } else {
        echo "Skip deploy"
    }

}