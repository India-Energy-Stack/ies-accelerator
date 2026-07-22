import os
import re

def slugify(text):
    slug = text.lower()
    slug = re.sub(r'<[^>]+>', '', slug)
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = slug.strip('-')
    return slug

def parse_headings(filepath):
    headings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        in_code_block = False
        for line in f:
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            
            # Match #, ##, ###
            match = re.match(r'^(#{1,5})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((level, title))
    return headings

def generate_file_entry(root_dir, rel_path, summary_text):
    full_path = os.path.join(root_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"Warning: File {rel_path} does not exist!")
        return f"* **[{os.path.basename(rel_path)}]({rel_path})** (Missing File)\n"
        
    headings = parse_headings(full_path)
    
    output = f"* **[{os.path.basename(rel_path)}]({rel_path})**\n"
    output += f"  - *Summary*: {summary_text}\n"
    if headings:
        output += "  <details>\n"
        output += "  <summary><b>Show Outline / Headings</b></summary>\n"
        
        current_level = 0
        for level, title in headings:
            anchor = slugify(title)
            href = f"{rel_path}#{anchor}"
            link = f'<a href="{href}">{title}</a>'
            
            if level > current_level:
                while level > current_level:
                    output += "  " * current_level + "  <ul>\n"
                    current_level += 1
                output += "  " * current_level + f"  <li>{link}"
            elif level < current_level:
                while level < current_level:
                    output += "\n" + "  " * (current_level - 1) + "  </li>\n"
                    output += "  " * (current_level - 1) + "  </ul>"
                    current_level -= 1
                output += "\n" + "  " * current_level + f"  <li>{link}"
            else:
                output += f"</li>\n" + "  " * current_level + f"  <li>{link}"
                
        while current_level > 0:
            output += "\n" + "  " * (current_level - 1) + "  </li>\n"
            output += "  " * (current_level - 1) + "  </ul>"
            current_level -= 1
            
        output += "\n  </details>\n"
    return output

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    sections = {
        "foundational": [
            ("README.md", "Root-level introduction to the IES accelerator repository structure, standard protocols, and setup environment."),
            ("getting-started.md", "A 5-minute technical orientation covering IES core capabilities, roles, prerequisites, and developer onboarding options."),
            ("glossary.md", "A comprehensive directory defining energy, decentralized identity (DIDs, VCs), and Beckn protocol terms."),
            ("faq.md", "Running list of common questions and answers about IES — drawn from the IES Technical Note's Annexure A."),
            ("download-pdf.md", "Where to download the auto-published, always-current printable PDF of this entire guide, and how to build it locally."),
            ("SUMMARY.md", "Table of Contents sidebar structure configuration for GitBook deployment.")
        ],
        "identifiers_setup": [
            ("what-ies-provides/register.md", "Single-page reference for the identity + directory layer: DID methods, the two identities, identifier patterns, DeDi registries, IES networks."),
            ("how-you-implement-ies/setup-register.md", "Role-based do-guide: domain, keypair, did.json, DeDi namespace; Beckn subscriber records and IES network references for network participants.")
        ],
        "credentials_setup": [
            ("how-you-implement-ies/issue-credentials.md", "Do-guide: run OpenCred with DeDi config, issue / verify / revoke, credential variants, verifier walkthrough, holder binding, operational notes."),
            ("what-ies-provides/energy-credentials/README.md", "Reference: credential lifecycle, the three IES credentials, variants, trust model, core concepts.")
        ],
        "credentials_ops": [
            ("how-you-implement-ies/digilocker.md", "DigiLocker delivery: Pull URI, callback flow, signature pinning.")
        ],
        "exchange_setup": [
            ("what-ies-provides/discover.md", "Single-page reference: the two rails (B2B data exchange vs B2C credentials), Beckn lifecycle, the IES networks."),
            ("what-ies-provides/exchange.md", "Single-page reference: the schemas, verifiable credentials, schemas by use case."),
            ("how-you-implement-ies/setup-exchange.md", "Do-guide: ONIX sandbox walkthrough, ngrok interop, real-identity swap, allowedNetworkIDs, test/prod separation, wire-level appendices.")
        ],
        "schemas_overview": [
            ("what-ies-provides/schemas-overview/README.md", "Plain-language overviews of each IES schema family — what it carries and when to use it, before the field-level reference."),
            ("what-ies-provides/schemas-overview/electricity-credential.md", "ElectricityCredential — plain-language overview."),
            ("what-ies-provides/schemas-overview/meter-data.md", "MeterData — plain-language overview."),
            ("what-ies-provides/schemas-overview/meter-data-credential.md", "MeterDataCredential — plain-language overview."),
            ("what-ies-provides/schemas-overview/meter-data-request.md", "MeterDataRequest — plain-language overview."),
            ("what-ies-provides/schemas-overview/meter-data-request-credential.md", "MeterDataRequestCredential — plain-language overview."),
            ("what-ies-provides/schemas-overview/arr-filing.md", "ArrFiling — plain-language overview."),
            ("what-ies-provides/schemas-overview/outage-notification.md", "OutageNotification — plain-language overview.")
        ],
        "usecases_overview": [
            ("use-cases-overview/README.md", "Shallow overviews of each IES use case — the business outcome and which schemas/rails it combines, before the implementation guide."),
            ("use-cases-overview/consumer-energy-passport.md", "Consumer Energy Passport — overview."),
            ("use-cases-overview/consumer-meter-digest.md", "Consumer Meter Digest — overview."),
            ("use-cases-overview/smart-meter-data-exchange.md", "Smart Meter Data Exchange — overview."),
            ("use-cases-overview/der-visibility.md", "DER Visibility — overview."),
            ("use-cases-overview/discom-regulatory-filing.md", "DISCOM Regulatory Filing — overview."),
            ("use-cases-overview/tariff-intelligence.md", "Tariff Intelligence — overview.")
        ],
        "schemas": [
            ("schemas/README.md", "Schemas — master schema map, plain-language overviews, standards precedence, versioning, and the proposal flow for new schemas."),
            ("schemas/ElectricityCredential/README.md", "ElectricityCredential family page — version history, inheritance, and usage."),
            ("schemas/ElectricityCredential/v1.2/README.md", "Auto-generated field reference for ElectricityCredential v1.2 (current)."),
            ("schemas/MeterData/v0.6/CHANGELOG.md", "Changelog detailing Form A and Form B dual-representation upgrades in MeterData v0.6."),
            ("schemas/MeterData/v0.6/README.md", "Detailed technical specification for the updated MeterData v0.6 dual-representation schemas."),
            ("schemas/MeterDataRequest/v0.6/README.md", "Field definitions and compilation guidelines for MeterDataRequest v0.6."),
            ("schemas/MeterDataRequestCredential/v0.1/README.md", "W3C Verifiable Credential wrapping a MeterDataRequest, enabling secure authorized requests."),
            ("schemas/ArrFiling/v0.5/README.md", "Detailed schema fields and validation steps for Annual Revenue Requirement filings v0.5.")
        ],
        "usecases": [
            ("use-cases/README.md", "Snapshot index of the IES Use Case Guides — each follows the IES Documentation Template."),
            ("use-cases/consumer-energy-passport/README.md", "Holder-bound ElectricityCredential v1.2 issued by a DISCOM into a consumer's wallet (DigiLocker)."),
            ("use-cases/consumer-meter-digest/README.md", "Holder-bound MeterDataCredential v0.6 — consumer's own meter readings on demand, signed by the DISCOM."),
            ("use-cases/smart-meter-data-exchange/README.md", "Implementer guide: AMISP/DISCOM/SERC/third-party telemetry exchange over IES Data Exchange, carrying the MeterData schema; includes the optional MeterDataRequestCredential consent flow."),
            ("use-cases/smart-meter-data-exchange/ies-meter-data-model.md", "Reference: Indian smart-metering terminology (OBIS, IS 15959 profiles and event IDs, CIM master data) mapped to the MeterData schema, with the IS 15959 deep-reference appendix."),
            ("use-cases/der-visibility/README.md", "Grid-side issuance of ElectricityCredential v1.2 — per-feeder view of every DER behind a DISCOM's meters."),
            ("use-cases/discom-regulatory-filing/README.md", "Publishing ARR datasets to State Electricity Regulatory Commissions."),
            ("use-cases/tariff-intelligence/README.md", "Publishing tariff rate structures and telescopic schedules as IES policies."),
            ("use-cases/p2p-energy-trading/README.md", "Inter-DISCOM prosumer-to-prosumer energy trade carried as a signed DEGContract over IES Data Exchange; network rules and the seller-DISCOM contract policy enforced as signed Rego, hosted on DeDi.")
        ],
        "pathways": [
            ("pathways/README.md", "Map of available role roadmaps in the IES ecosystem."),
            ("pathways/utility.md", "The chronological onboarding roadmap for a new utility (DISCOM) joining the network."),
            ("pathways/secretariat.md", "The operational roadmap for the Secretariat to approve registries, monitor networks, and maintain schemas."),
            ("pathways/authority.md", "The roadmap for a Ministry / CEA / SERC-CERC / Forum of Regulators reader — filings, tariff policy-as-code, and IES Cell governance."),
            ("pathways/tsp.md", "The roadmap for a Technology Service Provider (AMISP, OEM, integrator) building or configuring the IES adapter."),
            ("pathways/researcher.md", "The roadmap for a researcher or analyst studying IES using its published specs, examples and pilot outcomes."),
            ("contributors.md", "Acknowledgements — pilot DISCOMs, governance (IES Cell), and how to contribute.")
        ]
    }
    
    content = """# India Energy Stack (IES) Documentation Index

Welcome to the India Energy Stack (IES) documentation map. This index organizes all documentation files in the `ies-accelerator` repository sequentially and systematically by building blocks and phases.

---

## 📖 Foundational General References

These documents provide a general introduction, terminology definitions, and layout structures for the repository.

"""
    
    for rel_path, summary in sections["foundational"]:
        content += generate_file_entry(root_dir, rel_path, summary)
    
    content += """
---

## 🆔 1. Register — Identity and Directory (DIDs + DeDi)

This block defines the cryptographic identity of utilities, consumers, assets, and datasets, and the directories that resolve identifiers to participant records.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["identifiers_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🪪 2. Energy Credentials (VCs / OpenCred)

This block handles digital attestations of connections, billing summaries, and consumer identities.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["credentials_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)
        
    content += """
### 🔌 Use & Operations
"""
    for rel_path, summary in sections["credentials_ops"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🔌 3. Discover and Exchange (Beckn)

This block governs data discovery, consent, and the transfer of telemetry and regulatory datasets.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["exchange_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🗃️ 4. Schemas Overview

Plain-language overviews of each schema family and how the schemas fit together — the shallow layer above the field-level reference.

"""
    for rel_path, summary in sections["schemas_overview"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 📚 5. Schemas (field reference)

Each family page opens with a concise plain-language overview; version pages carry the auto-generated field reference.

"""
    for rel_path, summary in sections["schemas"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🧭 6. Use Case Overviews

Shallow, business-outcome overviews of each use case — what it delivers and which schemas/rails it combines.

"""
    for rel_path, summary in sections["usecases_overview"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🎯 7. Use Case Implementation Guides

Practical deployment and mapping implementations for specific grid business processes.

"""
    for rel_path, summary in sections["usecases"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🗺️ 8. Operational Pathways (Roadmaps)

Step-by-step project-management pathways for onboarding and network operations.

"""
    for rel_path, summary in sections["pathways"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    out_file = os.path.join(root_dir, "index.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("index.md compiled successfully with collapsible elements!")

if __name__ == '__main__':
    main()
