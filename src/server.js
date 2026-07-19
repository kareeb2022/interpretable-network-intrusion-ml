const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
app.use(express.json());

const PORT = 3000;

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy', timestamp: new Date() });
});

// Production Telemetry Prediction Endpoint
app.post('/api/telemetry', (req, res) => {
    const { cpu_usage_pct, memory_usage_pct, network_latency_ms, cpu_rolling_avg } = req.body;

    // Validate inputs
    if (cpu_usage_pct === undefined || memory_usage_pct === undefined || network_latency_ms === undefined || cpu_rolling_avg === undefined) {
        return res.status(400).json({ error: 'Missing metric fields in telemetry request packet.' });
    }

    // Call a swift Python micro-script to run inference using our serialized pkl model
    const pythonScriptPath = path.join(__dirname, 'predict_sub.py');
    const command = `python3 ${pythonScriptPath} ${cpu_usage_pct} ${memory_usage_pct} ${network_latency_ms} ${cpu_rolling_avg}`;

    exec(command, (error, stdout, stderr) => {
        if (error || stderr) {
            console.error(`Inference script execution failure: ${stderr || error.message}`);
            return res.status(500).json({ error: 'Internal processing error executing prediction inference model.' });
        }

        try {
            const predictionResult = JSON.parse(stdout.trim());
            res.status(200).json({
                timestamp: new Date(),
                failure_predicted: predictionResult.prediction === 1,
                risk_score: predictionResult.probability,
                action_required: predictionResult.prediction === 1 ? 'Immediate System Reboot / Failover Intervention' : 'None'
            });
        } catch (parseError) {
            res.status(500).json({ error: 'Failed to process model output formatting.' });
        }
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Production Telemetry Interface is live and listening on port ${PORT}`);
});