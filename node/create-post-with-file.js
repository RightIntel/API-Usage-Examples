const fs = require('node:fs');

async function main() {
    const now = new Date();
    const idx = 9;
    const pdfBuffer = fs.readFileSync(`${__dirname}/sample.pdf`);
    const domain = 'https://sharprua.com';
    const basicAuthToken = 'Insert base64 key from https://sharprua.com/developers/rest/overview/keys';

    const post = await fetch(`${domain}/api/v2/posts`, {
        method: 'POST',
        headers: {
            Authorization: `Basic ${basicAuthToken}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            headline: `My PDF post #${idx}`,
            publish: true,
            body: `This post was created via the API on ${now}`,
        }),
    });

    const postId = post.headers.get('API-New-Record-Id');

    if (!postId) {
        console.error('Error creating post:');
        console.log(`HTTP ${post.status} ${post.statusText}`);
        console.log(Object.fromEntries(post.headers.entries()));
        console.log(JSON.stringify(await post.text()));
        process.exit(1);
    }

    console.log(`HTTP ${post.status} - Created post with id ${postId} at ${domain}/p/${postId}`);

    const att = await fetch(`${domain}/api/v2/posts/${postId}/attachments`, {
        method: 'POST',
        headers: {
            Authorization: `Basic ${basicAuthToken}`,
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: `sample pdf ${idx}.pdf`,
            data: 'data:application/pdf;base64,' + pdfBuffer.toString('base64'),
        }),
    });

    const attId = att.headers.get('API-New-Record-Id');

    console.log(`HTTP ${att.status} - Added attachment with id ${attId} to post with id ${postId}`);

    console.log('headers:');

    console.log(Object.fromEntries(att.headers.entries()));
}

main().catch(console.error)