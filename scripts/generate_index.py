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
            ("SUMMARY.md", "Table of Contents sidebar structure configuration for GitBook deployment.")
        ],
        "identifiers_setup": [
            ("identifiers/README.md", "Introduction to the IES addressing layer, design principles, and role-based onboarding paths."),
            ("identifiers/concepts.md", "Cryptographic theory behind DIDs (did:web, did:key, did:dedi) and identifier vs. record separation."),
            ("identifiers/id-patterns.md", "Grammar conventions and syntax rules for minting identifiers for DISCOMs, consumers, regulators, and assets.")
        ],
        "identifiers_ops": [
            ("identifiers/issuance-reference.md", "Worked reference implementation (Python/OpenSSL) for key generation, did.json creation, and credential issuance."),
            ("checklists/identifiers-basic-checklist.md", "Self-audit checklist to verify domain ownership, key formats, and DID structures.")
        ],
        "registries_setup": [
            ("registries/README.md", "Introduction to the trust registry layer and related building blocks."),
            ("registries/dedi-primer.md", "Conceptual primer on Decentralized Directories, namespace control, and trust pillars."),
            ("registries/registry-creation.md", "Developer walkthrough for creating namespaces, verification, and managing DeDi records via UI/API."),
            ("registries/required-registries.md", "Detailed specification of schemas, record shapes, and onboarding channels for public/private registries."),
            ("registries/private_resolution.md", "Overview of public vs. private resolution and namespace layout conventions for DeDi tables.")
        ],
        "registries_ops": [
            ("registries/resolution.md", "Detailed specification of did:web, did:key, and did:dedi resolvers, error matrices, and caching rules."),
            ("checklists/registries-basic-checklist.md", "Auditing checklist to confirm namespace delegation, key records, and registry accessibility.")
        ],
        "credentials_setup": [
            ("energy-credentials/README.md", "Introduction to W3C Verifiable Credentials (VCs) in the energy sector and recommended reading order."),
            ("energy-credentials/concepts.md", "Concepts of credential roles (Issuer, Holder, Verifier), trust delegation, and DeDi revocation patterns."),
            ("energy-credentials/schemas.md", "Detailed breakdown of the electricity credential JSON schema and JSON-LD contexts."),
            ("energy-credentials/onboarding.md", "Step-by-step instructions for deploying OpenCred docker instances and setting up signing keys.")
        ],
        "credentials_ops": [
            ("energy-credentials/issuance.md", "Guide to mapping customer master data to the issue API, batch issuance, and lifecycle patterns."),
            ("energy-credentials/verification.md", "Specifications for verifying signatures, schema compliance, and DeDi revocation status list updates."),
            ("energy-credentials/digilocker-integration.md", "Integration guide for connecting OpenCred with India's DigiLocker Pull URI protocol."),
            ("energy-credentials/consumer-energy-passport.md", "Envelope specification and fields for the Consumer Energy Passport credential."),
            ("energy-credentials/consumer-meter-digest.md", "Envelope specification and readings structure for the Consumer Meter Digest credential."),
            ("checklists/energy-credentials-basic-checklist.md", "Basic check list for credential issuance and environment testing."),
            ("checklists/energy-credentials-checklist.md", "Overview readiness checklist for credential deployments."),
            ("checklists/energy-credentials-checklist-detailed.md", "Production implementation reference for key management, batching, and delivery.")
        ],
        "exchange_setup": [
            ("data-exchange/README.md", "Introduction to Beckn-based federated energy data exchange and network components."),
            ("data-exchange/concepts.md", "Just-enough theory: Beckn lifecycle, trust, DatasetItem, schema families, validation, stack topology."),
            ("data-exchange/quick-start.md", "Developer guide to starting local sandboxes and sending confirm -> on_confirm exchanges."),
            ("data-exchange/registry-setup.md", "Detailed steps for configuring ONIX with real identities and whitelisting namespaces."),
            ("data-exchange/appendix.md", "Reference detail: context invariants, validation dispatch, endpoints, sequence diagram.")
        ],
        "exchange_ops": [
            ("checklists/data-exchange-checklist.md", "Staged onboarding checklist from devkit sandbox to production go-live.")
        ],
        "schemas": [
            ("schemas/README.md", "Catalog of schemas, their purpose, versioning guidelines, and file structure."),
            ("schemas/ElectricityCredential/README.md", "Metadata, context inheritance, and fields for the ElectricityCredential VC schema."),
            ("schemas/ElectricityCredential/v1.0/README.md", "Technical specification and fields for Customer Credential v1.0."),
            ("schemas/MeterData/v0.5/README.md", "Overview and field representations for MeterData v0.5 profiles."),
            ("schemas/MeterData/v0.6/CHANGELOG.md", "Changelog detailing Form A and Form B dual-representation upgrades in MeterData v0.6."),
            ("schemas/MeterData/v0.6/README.md", "Detailed technical specification for the updated MeterData v0.6 dual-representation schemas."),
            ("schemas/MeterDataRequest/v0.6/README.md", "Field definitions and compilation guidelines for MeterDataRequest v0.6."),
            ("schemas/MeterDataRequestCredential/v0.1/README.md", "W3C Verifiable Credential wrapping a MeterDataRequest, enabling secure authorized requests."),
            ("schemas/ArrFiling/v0.5/README.md", "Detailed schema fields and validation steps for Annual Revenue Requirement filings v0.5.")
        ],
        "usecases": [
            ("use-cases/README.md", "Snapshot index of the six primary energy network use cases."),
            ("use-cases/smart-meter-data-exchange/README.md", "Implementer guide: AMISP/DISCOM/SERC/third-party telemetry exchange over IES Data Exchange, carrying the MeterData schema; includes the optional MeterDataRequestCredential consent flow."),
            ("use-cases/smart-meter-data-exchange/ies-meter-data-model.md", "Reference: Indian smart-metering terminology (OBIS, IS 15959 profiles and event IDs, CIM master data) mapped to the MeterData schema, with the IS 15959 deep-reference appendix."),
            ("use-cases/consumer-meter-digest/README.md", "Exchanging monthly meter digests via user consent and pull credentials."),
            ("use-cases/consumer-meter-digest/checklist.md", "Checklist for configuring consent endpoints and digest minting."),
            ("use-cases/consumer-energy-passport/README.md", "Consolidating generation, storage, and consumption VCs into a unified consumer passport."),
            ("use-cases/consumer-energy-passport/checklist.md", "Checklist for passport profiling, triggers, and wallet distribution."),
            ("use-cases/discom-regulatory-filing/README.md", "Publishing ARR datasets to State Electricity Regulatory Commissions."),
            ("use-cases/discom-regulatory-filing/checklist.md", "Checklist for regulatory cost mapping, adapter setup, and filing submissions."),
            ("use-cases/tariff-intelligence/README.md", "Publishing tariff rate structures and telescopic schedules as IES policies."),
            ("use-cases/tariff-intelligence/checklist.md", "Checklist for policy authoring, signing, and billing integration testing."),
            ("use-cases/energy-trading/README.md", "WIP — inter-discom prosumer-to-prosumer energy trade carried as a signed DEGContract over IES Data Exchange; network and settlement rules enforced by signed Rego bundles hosted on DeDi."),
            ("use-cases/energy-trading/checklist.md", "WIP — checklist for trading platforms, ledger providers, and discoms standing up energy trading.")
        ],
        "pathways": [
            ("pathways/README.md", "Map of available role roadmaps in the IES ecosystem."),
            ("pathways/utility.md", "The chronological onboarding roadmap for a new utility (DISCOM) joining the network."),
            ("pathways/secretariat.md", "The operational roadmap for the Secretariat to approve registries, monitor networks, and maintain schemas.")
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

## 🆔 1. Identifiers and Addressing (DIDs)

This block defines the cryptographic identity of utilities, consumers, assets, and datasets on the network.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["identifiers_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)
        
    content += """
### 🔌 Use & Operations
"""
    for rel_path, summary in sections["identifiers_ops"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🗄️ 2. Registries and Directories (DeDi)

This block describes the directories that store and resolve identifiers to participant records.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["registries_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)
        
    content += """
### 🔌 Use & Operations
"""
    for rel_path, summary in sections["registries_ops"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🪪 3. Energy Credentials (VCs / OpenCred)

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

## 🔌 4. Data Exchange (Beckn)

This block governs data discovery, consent, and the transfer of telemetry and regulatory datasets.

### ⚙️ Setup & Configuration
"""
    for rel_path, summary in sections["exchange_setup"]:
        content += generate_file_entry(root_dir, rel_path, summary)
        
    content += """
### 🔌 Use & Operations
"""
    for rel_path, summary in sections["exchange_ops"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🗃️ 5. Schemas

Detailed documentation for the JSON and JSON-LD schema formats used in the accelerator.

"""
    for rel_path, summary in sections["schemas"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🎯 6. Use Cases

Practical deployment and mapping implementations for specific grid business processes.

"""
    for rel_path, summary in sections["usecases"]:
        content += generate_file_entry(root_dir, rel_path, summary)

    content += """
---

## 🗺️ 7. Operational Pathways (Roadmaps)

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
