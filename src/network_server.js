const express = require('express');
const { exec } = require('child_process');

const app = express();
const PORT = 4000; // Running on 4000 to completely avoid previous port locks

app.use(express.json());

app.post('/api/network/inspect', (req, res) => {
    const { packet_len_var, sync_flag_count, duration_ms, byte_transfer_rate } = req.body;

    if (packet_len_var === undefined || sync_flag_count === undefined || duration_ms === undefined || byte_transfer_rate === undefined) {
        return res.status(400).json({ error: "Invalid Packet Payload Structure." });
    }

    // Call our python local explainable execution layer
    const cmd = `python3 src/predict_network.py ${packet_len_var} ${sync_flag_count} ${duration_ms} ${byte_transfer_rate}`;

    exec(cmd, (error, stdout, stderr) => {
        if (error || stderr) {
            console.error(`Execution error: ${stderr || error.message}`);
            return res.status(500).json({ error: "Security validation engine execution timeout." });
        }

        const lines = stdout.split('\n');
        const resultLine = lines.find(line => line.startsWith('RESULT:'));

        if (!resultLine) {
            return res.status(500).json({ error: "Malformed predictive tracking matrix." });
        }

        const [prediction, riskScore, explanationFlags] = resultLine.replace('RESULT:', '').trim().split(',');
        const isMalicious = parseInt(prediction) === 1;

        res.json({
            status: "processed",
            security_alert: isMalicious,
            malicious_probability: parseFloat(riskScore),
            mitigation_action: isMalicious ? "DROP_PACKET_AND_BAN_IP" : "ALLOW_ACCESS",
            explainable_ai_telemetry: {
                primary_risk_vectors: explanationFlags.split('|'),
                model_architecture: "Interpretable Gradient Boosting Tree Stack"
            }
        });
    });
});

app.listen(PORT, () => {
    console.log(`🛡️ Explainable Intrusion Prevention API live on local port ${PORT}`);
});