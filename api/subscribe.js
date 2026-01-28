export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email, keyword } = req.body;
    const apiKey = process.env.BREVO_API_KEY;

    if (!email || !apiKey) {
        return res.status(400).json({ error: 'Missing email or API key' });
    }

    try {
        const response = await fetch('https://api.brevo.com/v3/contacts', {
            method: 'POST',
            headers: {
                'api-key': apiKey,
                'content-type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                listIds: [57],
                updateEnabled: true,
                attributes: {
                    SOURCE: 'SignalEngines_LP',
                    INTEREST: keyword || 'General'
                }
            })
        });

        if (response.ok || response.status === 201 || response.status === 204) {
            return res.status(200).json({ success: true, message: 'Contact added' });
        }

        // Handle "already exists" logic if needed
        const errorData = await response.json();
        if (errorData.code === 'duplicate_parameter') {
            return res.status(200).json({ success: true, message: 'Contact updated' });
        }

        return res.status(500).json({ error: 'Provider error', details: errorData });

    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error', details: error.message });
    }
}
