import org.jenkinsci.plugins.pipeline.modeldefinition.Utils

node {
    checkout scm
    def appImg

    stage('Build') {
        appImg = docker.build("myapp:latest", "./")
    }

    appImg.inside {
        stage('Test') {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            junit 'test-reports/results.xml'
        }
    }

    env.SKIP_PROD = 'true'
    stage("Manual Approval") {
        try {
            timeout(time: 1, unit: 'MINUTES') {
                input(message: 'Lanjutkan ke tahap Deploy?', ok: 'Yes')
            }
            env.SKIP_PROD = 'false'
        } catch (Throwable e) {
            echo "Approval ignored"
            Utils.markStageSkippedForConditional('Manual Approval')
        }
    }
    
    stage('Deploy') {
        if (env.SKIP_PROD == 'true') {
            echo "Skip deploy"
            Utils.markStageSkippedForConditional('Deploy')
        } else {
            sh 'docker compose down -v'
            sh 'docker compose up -d'
            sh 'docker system prune -f'
        }
    }

}
