#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { TraductorKaqchikelFunctionsStack } from '../lib/traductor-kaqchikel-functions-stack';

const app = new cdk.App();
new TraductorKaqchikelFunctionsStack(app, 'MyPipelineStack', {
  env: {
    account: '111111111111',
    region: 'eu-west-1',
  }
});

app.synth();