#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { TraductorKaqchikelFunctionsStack } from '../lib/traductor-kaqchikel-functions-stack';

const app = new cdk.App();
new TraductorKaqchikelFunctionsStack(app, 'TraductorKaqchikelFunctionsStack', {
  env: {
    account: '842797708612',
    region: 'us-east-1',
  }
});

app.synth();