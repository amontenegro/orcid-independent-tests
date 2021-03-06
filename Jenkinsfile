node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'                                         , description: 'Branch name to work on'),
            string(name: 'test_server'           , defaultValue: 'qa.orcid.org'                                   , description: 'Base domain name to test'),
            string(name: 'user_login'            , defaultValue: 'ma_test_31052017'                               , description: 'Username'),
            string(name: 'user_pass'             , defaultValue: 'ma_test_31052017'                               , description: 'Password'),
            string(name: 'orcid_id'              , defaultValue: '0000-0002-6816-6010'                            , description: 'Latest orcid ID'),
            string(name: 'search_value'          , defaultValue: '31052017'                                       , description: 'Family name query format'),            
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/orcidclients.py'               , description: 'Properties file with predefined secrets')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        sh "rm -f orcid/properties.py"
        writeFile file: 'testinputs.py', text: "test_server=\"$test_server\"\nsearchValue=\"$search_value\"\norcidId=\"$orcid_id\"\nuser_login=\"$user_login\"\npassword=\"$user_pass\"\n"
        sh "cat $client_secrets_file testinputs.py > orcid/properties.py"
    }
    
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
        sh ". .py_env/bin/activate && pip2 install -r orcid/requirements.txt"
    }

    stage('Clean OrcidiD'){
        def cleanup_orcid_record = false
        try {
            timeout(time:20,unit:'SECONDS'){
                cleanup_orcid_record = input message: 'Would you like to clean up orcid record before continue ?', 
                                                  ok: 'Clean',
                                          parameters: [booleanParam(defaultValue: false, description: '', name: 'Clean ?')]
            }
        } catch(err){
            echo err.toString()
        }
        if (cleanup_orcid_record) {
            echo "Removing activities from orcid record [$orcid_id]"
            sh ". .py_env/bin/activate && pytest -v -r fEx orcid/api_read_delete.py"
        } else {
            echo "Continuing with existing record content."
        }
    }

    stage('Run Test Public Read'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_api_read_search.xml orcid/test_public_api_read_search.py"
                        
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Test 1.2 post'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member12_api_post_update.xml orcid/test_member12_api_post_update.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Test 2.0 post'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member20_api_post_update.xml orcid/test_member20_api_post_update.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Test Public Record'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_record.xml orcid/test_public_record.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Test Private Record'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_private_record.xml orcid/test_private_record.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Expected Errors Test'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_expected_errors.xml orcid/test_expected_errors.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Limited Record Test'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_limited_record.xml orcid/test_limited_record.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run 1.2 All Endpoints'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_12api_all_endpoints.xml orcid/test_12api_all_endpoints.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run 2.0 All Endpoints'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_20api_all_endpoints.xml orcid/test_20api_all_endpoints.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }          
    
    stage('Run Test scope methods'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_scope_methods.xml orcid/test_scope_methods.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
            deleteDir()
        }
    }    
}
