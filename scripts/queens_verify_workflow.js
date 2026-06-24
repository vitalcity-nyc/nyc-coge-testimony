export const meta = {
  name: 'coge-queens-name-verify',
  description: 'Verify Queens hearing witness names against public records',
  phases: [{ title: 'Verify', detail: 'One research agent per witness' }],
}

const witnesses = [{"name": "Deborah Green", "affiliation": "Resident of Long Island City, Queens; registered Democrat / longtime independent", "role_type": "Resident", "quote": "What better way to restore faith in government than by ending the longstanding disenfranchisement of almost a quarter of the electorate?"}, {"name": "Alan Cox", "affiliation": "Community health outreach worker with COAP (Coalition for Positive Health Empowerment); lifelong New Yorker, Bronx resident; independent voter", "role_type": "Nonprofit", "quote": "We have a system where 1.2 million folks who are independents are shut out of voting in the primaries. And that's where most decisions are made."}, {"name": "Robert Brown", "affiliation": "New York City resident, longtime taxpayer; identifies as independent (younger-generation voter)", "role_type": "Resident", "quote": "We all pay taxes, we all contribute to this city, we should all have a fair shot."}, {"name": "Anne Marie Gray", "affiliation": "Open New York, executive director (statewide pro-housing grassroots advocacy group)", "role_type": "Advocacy org", "quote": "We really must take a more well-rounded view of neighborhood character... so too are the New Yorkers that live in them."}, {"name": "Cordell Schachter", "affiliation": "Former NYC and federal government CTO/CIO; executive in residence at the Transit Tech Lab", "role_type": "Civic-tech", "quote": "Streamline IT hiring and workforce development via a multidisciplinary board working with state authorities, labor, academia and the private sector."}, {"name": "Honda Wang", "affiliation": "Ordinary New York City worker (rank-and-file civil servant), testifying in personal capacity", "role_type": "Labor", "quote": "Asking the charter commission to eliminate guardrails because of mismanagement would be the equivalent of asking the FAA to relax airline safety standards after a plane crash because of Boeing's mismanagement."}, {"name": "Zachary Thomas", "affiliation": "Member of the parks committee, Manhattan Community Board 3 (recently moved to Long Island City)", "role_type": "Government body", "quote": "Make it easier for Parks and other agencies to hire and retain quality candidates so resident-initiated projects actually get executed."}, {"name": "Phil Wong", "affiliation": "New York City Council Member, 30th District, Queens (Middle Village, Maspeth, Elmhurst, Ridgewood, Glendale, Rego Park)", "role_type": "Elected official", "quote": "Require cost-effectiveness reviews before signing billion-dollar contracts (e.g. emergency hotel shelters at $352/night) and tie contracts to real outcomes."}, {"name": "Payway", "affiliation": "Co-owner of Zazza restaurant (Southeast Asian community, Queens); board director of a NYC restaurant group", "role_type": "Business/industry", "quote": "Outdoor dining actually largely become a luxury for the well-funded restaurant in a wealthy neighborhood."}, {"name": "Helen Zhang", "affiliation": "Owner of Ziggy's Roman Cafe, a full-service restaurant at 15 Main Street, Dumbo, Brooklyn (testified online)", "role_type": "Business/industry", "quote": "I spent five months fighting for the right to put tables outside my front door. Please, I would love to make sure no one else does the same."}, {"name": "Michael Kelly", "affiliation": "Outdoor-dining permit expediter who filed 400+ sidewalk, roadway and closed-cafe applications for clients (testified online)", "role_type": "Business/industry", "quote": "The main complaint is that they paid the fee and cannot operate."}, {"name": "Megan Rickerson", "affiliation": "Owner of Someday Bar in Boerum Hill, Brooklyn (testified online)", "role_type": "Business/industry", "quote": "If we're waiting six plus months to get going, think about how many restaurants and bars just missed out... So much revenue was lost from small businesses that people really, really needed."}, {"name": "Sumana Harihareswara", "affiliation": "Software professional (testified online); cited beta NYC and 18F", "role_type": "Civic-tech", "quote": "When we buy or build software that only a few people can ever improve or look at because it's closed source, then that reduces efficiency."}, {"name": "Ligia Gualpa", "affiliation": "Workers Justice Project, executive director (delivery and day-laborer organizing)", "role_type": "Advocacy org", "quote": "The Deliverista Hubs are the solution, are the model to look at for what public safety solutions should look like."}, {"name": "Antonio Solis", "affiliation": "Delivery worker, member of the Workers Justice Project (testified in Spanish via interpreter)", "role_type": "Labor", "quote": "In reality, the streets have become our place of work, but every day we encounter and face danger due to the lack of safe infrastructure."}, {"name": "Frank Morano", "affiliation": "New York City Council Member, Staten Island South Shore (testified online)", "role_type": "Elected official", "quote": "People don't care how many meetings were held. They care whether their pothole was filled."}, {"name": "Ashley Graber", "affiliation": "Co-owner of Cool Hand Movers, a Brooklyn-based licensed moving company (testified online)", "role_type": "Business/industry", "quote": "The city does recognize that these tickets are unavoidable, but they then treat it as a reliable revenue stream."}, {"name": "Rajesh Sankat", "affiliation": "Program strategist and civic designer at three by three, a community-centered design studio in Brooklyn", "role_type": "Civic-tech", "quote": "When something shapes all of our lives, we don't leave it entirely to private actors. And that is what is happening with AI."}, {"name": "Pritya Shrimali", "affiliation": "Recent NYC high school graduate and New Jersey resident researching federal superfund and urban environmental remediation policy", "role_type": "Academic", "quote": "A child born in this neighborhood today will be finishing elementary school before the cleanup even begins."}, {"name": "Mary Anil", "affiliation": "Astoria, Queens resident (29 years); NYC government employee since 2007; MPA from Baruch, PhD from CUNY Graduate Center", "role_type": "Resident", "quote": "If many incumbents are running for other offices in competitive elections and are campaigning for six or ten months, then I worry about our governance."}, {"name": "Damian Archibald", "affiliation": "Anesthesiologist at Elmhurst Hospital, Queens; resident of Long Island City", "role_type": "Labor", "quote": "The state of our public spaces and roads are a public health issue."}, {"name": "Henry Smith", "affiliation": "Director of economic development, Long Island City Partnership / LIC Business Improvement District (testified online)", "role_type": "Business/industry", "quote": "It has really been a problem with not only just cases being closed immediately but also to have the follow-up."}, {"name": "India Bee", "affiliation": "Local beekeeper; founder of a sensory-inclusion pop-up organization; parent and disability advocate (CUNY graduate degree in disability studies)", "role_type": "Advocacy org", "quote": "The city is beautiful, noisy chaos, and a lot of our loved ones cannot function in that... allow us to hold on to the pole and support our loved ones."}, {"name": "Taiwan Green", "affiliation": "Music educator, community advocate and small business owner; lifelong resident of Southeast Queens", "role_type": "Resident", "quote": "We were very hard to remove litter and improve the area. Unfortunately, by the very next day, it looked as though we had never been there."}, {"name": "Terry Renee", "affiliation": "Community health worker who attends public hearings across New York City", "role_type": "Resident", "quote": "If a resource is not being used... you might as well not have it exist. It's the same thing as if it doesn't exist because you can't navigate it."}];

const SCHEMA = {
  type:'object',
  properties:{
    original_name:{type:'string'},
    corrected_name:{type:'string'},
    name_verified:{type:'boolean'},
    name_confidence:{type:'string', enum:['high','medium','low']},
    affiliation_corrected:{type:'string'},
    verify_source:{type:'string'},
    notes:{type:'string'}
  },
  required:['original_name','corrected_name','name_verified','name_confidence']
}

phase('Verify')
log(`Verifying ${witnesses.length} Queens witnesses against public records`)

const results = await parallel(witnesses.map(w => () =>
  agent(
    `Verify the real identity of a witness who testified at the NYC Commission on Government Efficiency (COGE) Round 1 QUEENS hearing on June 22, 2026. The name below was auto-transcribed by speech-to-text (Whisper) and may be MISSPELLED or garbled.

Transcribed name: "${w.name}"
Stated affiliation/role (also from the transcript, may be imperfect): ${w.affiliation}
Role type: ${w.role_type}
A line from their testimony (for disambiguation): "${w.quote}"

Your task: find this person in public records and determine the CORRECT spelling of their name and an accurate affiliation.

Search strategies:
- Search the affiliation/organization + the role to find the real person.
- Search the distinctive content of their quote.
- Check org staff/leadership pages, LinkedIn, news coverage, council/government rosters.
- For elected officials, confirm against the official roster.
- Well-known civic-tech / advocacy figures may already be spelled correctly (do NOT "correct" a name that is actually right).

Rules:
- If you CONFIRM the person via a public record: name_verified=true, corrected_name = correct spelling, name_confidence="high", give verify_source (URL/specific source) + corrected affiliation.
- If you find a LIKELY but unconfirmed match: name_verified=false, name_confidence="medium", explain in notes.
- If an ordinary resident with no findable footprint: keep the transcribed name, name_verified=false, name_confidence "low" (garbled) or "medium" (ordinary plausible), say so. Do NOT invent an identity.
- Never fabricate a source.

Return original_name="${w.name}", corrected_name, name_verified, name_confidence, affiliation_corrected, verify_source, notes.`,
    { label: w.name.slice(0,22), phase:'Verify', schema: SCHEMA }
  )
))

const r = results.filter(Boolean)
const changed = r.filter(x => x.corrected_name && x.corrected_name.trim().toLowerCase() !== x.original_name.trim().toLowerCase())
const verified = r.filter(x => x.name_verified)
log(`Verified ${verified.length}/${witnesses.length}; ${changed.length} corrections`)

return { results: r, corrections: changed.map(x=>`${x.original_name} -> ${x.corrected_name} [${x.name_confidence}]`) }
